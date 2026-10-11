#!/usr/bin/env python3
"""QA pass 2 for essentialelements manual pages (en + zh).

Fixes (never touching fenced code bodies, never translating):
  1. Half-converted MyST list-tables (`| Item | Value |` / `| 项目 | 内容 |`
     fake headers + `* -` / `- ` bullet cells) -> real pipe tables, bullet
     lists (1-col), or display math (single math cell). House style: pipe
     table indented under `!!! note "caption"`.
  2. Orphan Sphinx field lines (:class: :header-rows: :widths: ...) removed;
     `:class: tip|warning|info|important|...` folds into the admonition kind.
  3. Math: blank lines inside `$$...$$` removed (arithmatex needs one
     paragraph); multi-line inline `$...$` spans joined to one line.
  4. `sec:` links: pretty link text (last two id segments); bare `](sec:...)`
     and cross-page `](#sec:...)` rewritten to proper relative targets.
  5. Empty fences dropped (none expected).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs")
EE = "manual/contents/essentialelements"
FILES = [
    "index_essentialelements.md", "RI.md", "basics.md", "basisset.md",
    "coordinates.md", "counterpoise.md", "cpscf.md", "finEfield.md",
    "fragmentation.md", "frozencore.md", "initialguess.md", "input.md",
    "integralhandling.md", "numericalgradients.md", "numericalintegration.md",
    "output.md", "parallel.md", "relativistic.md", "scf.md", "shark.md",
    "solvationmodels.md", "stabilityanalysis.md", "symmetry.md",
]

FAKE_HEADER = {"en": "| Item | Value |", "zh": "| 项目 | 内容 |"}
FAKE_SEP = "| --- | --- |"
PLACEHOLDER = {"en": "—", "zh": "无"}

FIELD_RE = re.compile(
    r"^[ \t]*:(?:width|class|header-rows|subcaptions|class-grid|align|scale"
    r"|name|alt|figwidth|figclass|option|stub-columns|widths|alignments):[^\n]*$"
)
ADMON_RE = re.compile(
    r'^(!!!\s+(?P<kind>note|tip|warning|info|abstract|success|question|failure|bug|example|quote))'
    r'(?P<title>\s+"(?P<t>[^"]*)")?[ \t]*$'
)
FENCE_RE = re.compile(r"^([ \t]*)(`{3,})(.*)$")
CLASS_KINDS = {
    "tip", "warning", "info", "abstract", "success", "question",
    "failure", "bug", "example", "quote", "hint", "attention",
    "caution", "danger", "error", "note",
}

report: dict[str, list[str]] = {}
LABEL_MAP: dict[str, str] = {}


def note(path: Path, msg: str) -> None:
    report.setdefault(str(path), []).append(msg)


# ============================================================ fence helpers
def fence_mask(lines: list[str]) -> list[bool]:
    """True where line is inside a fenced code block (including delimiters)."""
    mask = [False] * len(lines)
    stack: list[tuple[int, int]] = []
    for i, ln in enumerate(lines):
        m = FENCE_RE.match(ln)
        if m:
            marker = m.group(2)
            rest = m.group(3).strip()
            if not stack:
                stack.append((i, len(marker)))
                mask[i] = True
            else:
                _oi, om = stack[-1]
                if rest == "" and len(marker) >= om:
                    stack.pop()
                    mask[i] = True
                else:
                    stack.append((i, len(marker)))
                    mask[i] = True
            continue
        if stack:
            mask[i] = True
    return mask


# ============================================================ junk tables
def strip_outer_bold(cell: str) -> str:
    c = cell.strip()
    if len(c) >= 4 and c.startswith("**") and c.endswith("**"):
        inner = c[2:-2]
        # only strip one pair if the remainder doesn't start/end with unmatched *
        return inner.strip()
    return c


def esc_pipe(cell: str) -> str:
    return cell.replace("|", "\\|").strip()


def join_cell_lines(parts: list[str]) -> str:
    if not parts:
        return ""
    text = parts[0]
    for p in parts[1:]:
        if text.endswith("\\"):
            text = text[:-1].rstrip() + "<br>" + p
        else:
            text = text.rstrip() + " " + p
    return text.strip()


class JunkParser:
    """Parse a region of half-converted list-table junk into rows of cells."""

    def __init__(self, lines: list[str], lang: str, start: int):
        self.lines = lines
        self.lang = lang
        self.i = start
        self.n = len(lines)
        self.rows: list[list[str]] = []
        self.header_rows = 1  # default; caller may override from :header-rows:

    def _is_fake_header(self, ln: str) -> bool:
        return ln.strip() == FAKE_HEADER[self.lang]

    def _is_fake_sep(self, ln: str) -> bool:
        return ln.strip() == FAKE_SEP

    def _parse_fake_first(self, ln: str) -> str | None:
        """Line shaped `| **X** | — |` -> X (bold stripped). None if not."""
        s = ln.rstrip()
        m = re.match(r"^\| (.*\*.*) \| (?:—|无) \|$", s)
        if not m:
            return None
        return strip_outer_bold(m.group(1))

    @staticmethod
    def _strip_span_roles(text: str) -> str:
        text = re.sub(r"\{[cr]span\}`\d+`", "", text)
        text = re.sub(r"\s{2,}", " ", text).strip()
        # section-header style *Title* -> **Title**
        if re.fullmatch(r"\*[^*]+\*", text):
            text = "**" + text[1:-1] + "**"
        return text

    def _is_bullet(self, ln: str) -> tuple[int, str] | None:
        m = re.match(r"^([ \t]+)-[ \t]*(.*)$", ln.rstrip())
        if m and not ln.lstrip().startswith("- "):
            pass
        if m:
            ind = len(m.group(1))
            rest = m.group(2)
            # reject markdown list items at shallow indent outside table cells
            return ind, rest
        m2 = re.match(r"^([ \t]+)-$", ln.rstrip())
        if m2:
            return len(m2.group(1)), ""
        return None

    def _is_star_row(self, ln: str) -> tuple[int, str] | None:
        m = re.match(r"^([ \t]*)\* -[ \t]*(.*)$", ln.rstrip())
        if m:
            return len(m.group(1)), m.group(2)
        return None

    def parse(self) -> int:
        """Parse junk from self.i. Returns index after region."""
        cur_row: list[str] = []
        cur_cell: list[str] | None = None
        cell_indent: int | None = None
        in_row = False
        mode = "want_group"  # want_group | after_first | in_cells

        def flush_cell() -> None:
            nonlocal cur_cell
            if in_row and cur_cell is not None:
                cur_row.append(join_cell_lines(cur_cell))
            cur_cell = None

        def flush_row() -> None:
            nonlocal cur_row, in_row, cur_cell
            if not in_row:
                return
            flush_cell()
            if cur_row:
                self.rows.append(cur_row)
            cur_row = []
            in_row = False

        while self.i < self.n:
            ln = self.lines[self.i]
            stripped = ln.strip()

            # ---- start of a new fake group (header+sep+first)
            if self._is_fake_header(ln):
                if self.i + 2 < self.n and self._is_fake_sep(self.lines[self.i + 1]):
                    first = self._parse_fake_first(self.lines[self.i + 2])
                    if first is not None:
                        flush_row()
                        cur_row = [self._strip_span_roles(first)]
                        in_row = True
                        cell_indent = None
                        mode = "after_first"
                        self.i += 3
                        continue
                break

            if stripped == "":
                self.i += 1
                continue

            # ---- consecutive fake-first line -> new row
            ff = self._parse_fake_first(ln) if mode != "want_group" else None
            if ff is not None and mode in ("after_first", "in_cells"):
                # only if this looks like a junk placeholder row (not cell text)
                flush_row()
                cur_row = [self._strip_span_roles(ff)]
                in_row = True
                cell_indent = None
                mode = "after_first"
                self.i += 1
                continue

            # ---- continuation-row marker `* -`
            st = self._is_star_row(ln)
            if st is not None:
                flush_row()
                content = st[1].strip()
                cur_row = [self._strip_span_roles(content) if content else ""]
                in_row = True
                mode = "in_cells"
                self.i += 1
                continue

            # ---- bullet cell
            b = self._is_bullet(ln)
            if b is not None:
                ind, rest = b
                rest = self._strip_span_roles(rest)
                if mode == "after_first":
                    cell_indent = ind
                    mode = "in_cells"
                    cur_cell = [rest]
                    self.i += 1
                    continue
                if mode == "in_cells" and cell_indent is not None:
                    if ind == cell_indent:
                        flush_cell()
                        cur_cell = [rest]
                        self.i += 1
                        continue
                    if ind > cell_indent:
                        if cur_cell is None:
                            cur_cell = [ln.strip()]
                        else:
                            cur_cell.append(ln.strip())
                        self.i += 1
                        continue
                # bullet at unexpected indent -> end region
                break

            # ---- other indented line
            indent = len(ln) - len(ln.lstrip())
            if mode == "after_first" and indent > 0:
                # continuation of the (possibly multi-line) first cell
                cur_row[0] = (cur_row[0] + " " + ln.strip()).strip()
                self.i += 1
                continue
            if mode == "in_cells" and cell_indent is not None and indent > 0:
                if cur_cell is None:
                    cur_cell = [ln.strip()]
                else:
                    cur_cell.append(ln.strip())
                self.i += 1
                continue

            break

        flush_row()
        return self.i


def looks_like_math_rows(rows: list[list[str]]) -> bool:
    if len(rows) != 1 or len(rows[0]) != 1:
        return False
    c = rows[0][0]
    return c.startswith("$") or "\\begin{array}" in c or "\\begin{aligned}" in c


def rows_to_pipe(rows: list[list[str]], header_rows: int) -> list[str]:
    ncols = max((len(r) for r in rows), default=0)
    if ncols == 0:
        return []
    grid = [r + [""] * (ncols - len(r)) for r in rows]

    def line(r: list[str]) -> str:
        return "| " + " | ".join(esc_pipe(c) for c in r) + " |"

    out: list[str] = []
    if header_rows <= 0:
        out.append(line([""] * ncols))
        out.append("| " + " | ".join("---" for _ in range(ncols)) + " |")
        data = grid
    else:
        hdr = min(header_rows, len(grid))
        head = []
        for c in range(ncols):
            parts = [grid[r][c] for r in range(hdr) if grid[r][c].strip()]
            head.append("<br>".join(parts))
        out.append(line(head))
        out.append("| " + " | ".join("---" for _ in range(ncols)) + " |")
        data = grid[hdr:]
    for r in data:
        out.append(line(r))
    return out


def rows_to_bullets(rows: list[list[str]]) -> list[str]:
    out = []
    for r in rows:
        for c in r:
            if c.strip():
                out.append(f"* {c.strip()}")
    return out


def rows_to_math(rows: list[list[str]]) -> list[str]:
    cell = rows[0][0].strip()
    # unwrap single $...$ wrapper spanning the cell
    if cell.startswith("$") and cell.endswith("$") and not cell.startswith("$$"):
        inner = cell[1:-1].strip()
    else:
        inner = cell
    return ["$$", inner, "$$"]


# ============================================================ frozencore
def original_frozencore_rows() -> list[list[str]]:
    """Parse the original MyST list-table (empty cells preserved)."""
    src = Path(
        "/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/crawl/manual"
        "/_sources/contents/essentialelements/frozencore.md.txt"
    )
    text = src.read_text(encoding="utf-8")
    m = re.search(
        r"^:{3,}\{list-table\}.*?\n(?P<body>.*?)^:{3,}[ \t]*$",
        text,
        re.M | re.S,
    )
    if not m:
        raise SystemExit("frozencore list-table not found in original source")
    rows: list[list[str]] = []
    for ln in m.group("body").splitlines():
        if not ln.strip() or ln.lstrip().startswith(":"):
            continue
        mr = re.match(r"^\* -[ \t]*(.*)$", ln)
        if mr:
            rows.append([mr.group(1).strip()])
            continue
        mc = re.match(r"^[ \t]+-[ \t]*(.*)$", ln)
        if mc and rows:
            rows[-1].append(mc.group(1).strip())
    return rows


def rebuild_frozencore_block() -> list[str]:
    return rows_to_pipe(original_frozencore_rows(), 0)


def strip_span_roles_text(text: str) -> str:
    return re.sub(r"\{[cr]span\}`\d+`", "", text)


# ============================================================ source tables
SRC_ROOT = Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/md/manual")
SRC_DIRECTIVE_RE = re.compile(
    r"^:{3,}\{(?:flat-table|list-table)\}[ \t]*(?P<title>[^\n]*)\n"
    r"(?P<body>.*?)^:{3,}[ \t]*$",
    re.M | re.S,
)
SPAN_RE = re.compile(r"\{([cr])span\}`(\d+)`")


def _strip_spans(text: str) -> tuple[str, int, int]:
    cspan = rspan = 0

    def repl(m: re.Match) -> str:
        nonlocal cspan, rspan
        n = int(m.group(2))
        if m.group(1) == "c":
            cspan = n
        else:
            rspan = n
        return ""

    content = SPAN_RE.sub(repl, text)
    content = re.sub(r"  +", " ", content).strip()
    return content, cspan + 1, rspan + 1


def _parse_src_rows(body: str) -> list[list[tuple[str, int, int]]]:
    rows: list[list[tuple[str, int, int]]] = []
    for line in body.splitlines():
        if not line.strip() or line.lstrip().startswith(":"):
            continue
        m_row = re.match(r"^\s*\* -[ \t]*(.*)$", line)
        if m_row:
            content, cs, rs = _strip_spans(m_row.group(1))
            rows.append([(content, cs, rs)])
            continue
        m_cell = re.match(r"^[ \t]+-[ \t]*(.*)$", line)
        if m_cell and rows:
            content, cs, rs = _strip_spans(m_cell.group(1))
            rows[-1].append((content, cs, rs))
            continue
        # multi-line continuation of the current cell (math etc.)
        if rows and rows[-1]:
            text, cs, rs = rows[-1][-1]
            joined = (text + " " + line.strip()).strip()
            rows[-1][-1] = (joined, cs, rs)
    return rows


def _clean_cell_text(text: str) -> str:
    """Convert leftover MyST inline roles inside source table cells."""

    def ref(m: re.Match) -> str:
        inner = m.group(1)
        if "<" in inner and inner.endswith(">"):
            t, _, lab = inner.rpartition("<")
            return f"[{t.strip()}](#{lab[:-1].strip()})"
        return f"[{inner}](#{inner})"

    text = re.sub(r"\{ref\}`([^`]+)`", ref, text)
    text = re.sub(r"\{numref\}`([^`]+)`", ref, text)
    text = re.sub(
        r"\{cite\}`([^`]+)`",
        lambda m: f"[{m.group(1)}](../../bibliography.md)",
        text,
    )
    text = re.sub(r"\{eq\}`([^`]+)`", lambda m: f"[式 ({m.group(1)})](#{m.group(1)})", text)
    text = re.sub(r"\{index\}`[^`]*`", "", text)
    text = re.sub(r"\{download\}`([^`]+)`", r"`\1`", text)
    text = re.sub(r"\{[cr]span\}`\d+`", "", text)
    return text.strip()


def _build_src_grid(rows: list[list[tuple[str, int, int]]]) -> list[list[str]]:
    if not rows:
        return []
    ncols = max(sum(cs for _, cs, _ in r) for r in rows)
    grid: list[list[str | None]] = [[None] * ncols for _ in rows]
    for ri, cells in enumerate(rows):
        ci = 0
        for text, cs, rs in cells:
            while ci < ncols and grid[ri][ci] is not None:
                ci += 1
            if ci >= ncols:
                break
            for dr in range(rs):
                for dc in range(cs):
                    rj, cj = ri + dr, ci + dc
                    if rj < len(grid) and cj < ncols:
                        grid[rj][cj] = (
                            _clean_cell_text(text) if (dr == 0 and dc == 0) else ""
                        )
            ci += cs
    return [[c if c is not None else "" for c in row] for row in grid]


def extract_source_tables(lang: str, fn: str) -> list[dict]:
    src = SRC_ROOT / lang / "contents" / "essentialelements" / fn
    if not src.exists():
        return []
    text = src.read_text(encoding="utf-8")
    out = []
    for m in SRC_DIRECTIVE_RE.finditer(text):
        title = m.group("title").strip()
        body = m.group("body")
        header_rows = 0
        lines = body.splitlines()
        body_start = 0
        for i, ln in enumerate(lines):
            s = ln.strip()
            if s.startswith(":header-rows:"):
                try:
                    header_rows = int(s.split(":", 2)[2].strip())
                except ValueError:
                    header_rows = 1
                body_start = i + 1
            elif s.startswith(":") and not s.startswith(":-"):
                body_start = i + 1
            elif s.startswith("*"):
                break
        cell_body = "\n".join(lines[body_start:])
        rows = _parse_src_rows(cell_body)
        if not rows:
            continue
        grid = _build_src_grid(rows)
        out.append({"title": title, "header_rows": header_rows, "grid": grid})
    return out


def grid_to_pipe_src(grid: list[list[str]], header_rows: int) -> list[str]:
    if not grid:
        return []
    ncols = len(grid[0])

    def line(r: list[str]) -> str:
        return "| " + " | ".join(esc_pipe(c) for c in r) + " |"

    out: list[str] = []
    if header_rows <= 0:
        out.append(line([""] * ncols))
        out.append("| " + " | ".join("---" for _ in range(ncols)) + " |")
        data = grid
    else:
        hdr = min(header_rows, len(grid))
        head = []
        for c in range(ncols):
            parts = [grid[r][c] for r in range(hdr) if grid[r][c].strip()]
            head.append("<br>".join(parts))
        out.append(line(head))
        out.append("| " + " | ".join("---" for _ in range(ncols)) + " |")
        data = grid[hdr:]
    for r in data:
        out.append(line(r))
    return out


def is_junk_header(ln: str, lang: str) -> bool:
    return ln.strip() == FAKE_HEADER[lang]


def find_junk_regions(lines: list[str], lang: str) -> list[tuple[int, int]]:
    """Return (start, end) spans of junk table regions (end exclusive)."""
    mask = fence_mask(lines)
    regions: list[tuple[int, int]] = []
    i = 0
    n = len(lines)
    while i < n:
        if mask[i] or not is_junk_header(lines[i], lang):
            i += 1
            continue
        parser = JunkParser(lines, lang, i)
        end = parser.parse()
        if parser.rows:
            regions.append((i, end))
        i = max(end, i + 1)
    return regions


def replace_tables_from_source(lines: list[str], lang: str, fn: str, path: Path) -> list[str]:
    """Rebuild junk tables from the MyST source (empty cells preserved)."""
    tables = extract_source_tables(lang, fn)
    regions = find_junk_regions(lines, lang)
    if not regions:
        return lines
    if len(tables) != len(regions):
        note(
            path,
            f"source/junk table count mismatch ({len(tables)} vs {len(regions)}); "
            f"using junk parser fallback",
        )
        return process_junk_regions(lines, lang, path)

    out: list[str] = []
    prev_end = 0
    for idx, ((start, end), tbl) in enumerate(zip(regions, tables)):
        out.extend(lines[prev_end:start])
        grid = tbl["grid"]
        # single math cell -> display $$ block at column 0 (arithmatex
        # silently disables indented $$; pipe tables break on | in arrays)
        if (
            len(grid) == 1
            and len(grid[0]) == 1
            and (
                grid[0][0].strip().startswith("$")
                or "\\begin{array}" in grid[0][0]
                or "\\begin{aligned}" in grid[0][0]
            )
        ):
            cell = grid[0][0].strip()
            if cell.startswith("$") and cell.endswith("$") and not cell.startswith("$$"):
                inner = cell[1:-1].strip()
            else:
                inner = cell
            content = ["$$", inner, "$$"]
            note(path, f"L{start+1}: source math table #{idx+1} -> $$ block")
            # drop preceding field lines; keep admonition header but do not
            # indent math (must be column 0)
            while out and FIELD_RE.match(out[-1]):
                note(path, f"dropped field line before source table: {out[-1].strip()}")
                out.pop()
                while out and out[-1].strip() == "":
                    out.pop()
            for nl in content:
                out.append(nl)
            out.append("")
            prev_end = end
            continue

        content = grid_to_pipe_src(grid, tbl["header_rows"])
        note(
            path,
            f"L{start+1}: source table #{idx+1} "
            f"({len(grid)} rows, hdr={tbl['header_rows']})",
        )
        # indent under a preceding admonition if present
        indent = ""
        k = len(out) - 1
        while k >= 0 and out[k].strip() == "":
            k -= 1
        if k >= 0:
            prev = out[k]
            if ADMON_RE.match(prev) or prev.startswith("!!!"):
                indent = "    "
            elif FIELD_RE.match(prev):
                indent = "    "
            elif prev.startswith("    ") and FIELD_RE.match(prev):
                indent = "    "
        # drop immediately-preceding field lines (they'll be cleaned later too)
        while out and FIELD_RE.match(out[-1]):
            note(path, f"dropped field line before source table: {out[-1].strip()}")
            out.pop()
            while out and out[-1].strip() == "":
                out.pop()
        for nl in content:
            out.append((indent + nl) if indent else nl)
        out.append("")
        prev_end = end
    out.extend(lines[prev_end:])
    return out


# ============================================================ MyST fences
def fix_myst_fences(lines: list[str], path: Path) -> list[str]:
    """Convert leftover ```{subfigure} / ```{bibliography} fences."""
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        m = re.match(r"^```(?P<kind>\{(?:subfigure|bibliography)\})(?P<rest>.*)$", ln)
        if not m:
            out.append(ln)
            i += 1
            continue
        kind = m.group("kind")
        # collect body until closing ```
        j = i + 1
        body: list[str] = []
        closed = False
        while j < n:
            if re.match(r"^```\s*$", lines[j]):
                closed = True
                break
            body.append(lines[j])
            j += 1
        if not closed:
            out.append(ln)
            i += 1
            continue

        if "subfigure" in kind:
            imgs: list[str] = []
            caption_lines: list[str] = []
            for b in body:
                s = b.strip()
                if s.startswith(":") or not s:
                    continue
                if s.startswith("!"):
                    # rewrite image path to house style
                    mm = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", s)
                    if mm:
                        alt, pth = mm.group(1), mm.group(2)
                        fname = pth.split("/")[-1]
                        imgs.append(f"![{alt or fname}](../../../images/manual/{fname})")
                    else:
                        imgs.append(s)
                else:
                    caption_lines.append(s)
            out.extend(imgs)
            if caption_lines:
                out.append("")
                out.append("*" + " ".join(caption_lines) + "*")
            note(path, f"L{i+1}: ```{{subfigure}} -> {len(imgs)} image(s) + caption")
        else:  # bibliography
            keys = [b.strip() for b in body if b.strip() and not b.strip().startswith(":")]
            for k, key in enumerate(keys, 1):
                out.append(f"{k}. [{key}](../../bibliography.md)")
            note(path, f"L{i+1}: ```{{bibliography}} -> {len(keys)} linked key(s)")
        out.append("")
        i = j + 1
    return out


# ============================================================ process file
def process_junk_regions(lines: list[str], lang: str, path: Path) -> list[str]:
    """Replace every junk table region with a proper pipe table / bullets / math."""
    out: list[str] = []
    i = 0
    n = len(lines)
    mask = fence_mask(lines)
    while i < n:
        if mask[i]:
            out.append(lines[i])
            i += 1
            continue

        ln = lines[i]
        # detect start: fake header + sep + fake-first
        if ln.strip() == FAKE_HEADER[lang] and i + 2 < n:
            if lines[i + 1].strip() == FAKE_SEP:
                parser = JunkParser(lines, lang, i)
                end = parser.parse()
                rows = parser.rows
                if not rows:
                    out.append(lines[i])
                    i += 1
                    continue

                # find nearest preceding :header-rows: (already collected by
                # caller into parser.header_rows via scan below)
                # look backwards in `out` for field lines / admonition
                header_rows = 1
                k = len(out) - 1
                while k >= 0:
                    s = out[k].strip()
                    if s == "":
                        k -= 1
                        continue
                    m = re.match(r"^:header-rows:[ \t]*(\d+)", s)
                    if m:
                        header_rows = int(m.group(1))
                        break
                    if FIELD_RE.match(out[k]) or ADMON_RE.match(out[k]) or out[k].startswith("!!!"):
                        k -= 1
                        continue
                    break

                if looks_like_math_rows(rows):
                    new = rows_to_math(rows)
                    note(path, f"L{i+1}: math-cell junk -> $$ block")
                elif max(len(r) for r in rows) <= 1:
                    new = rows_to_bullets(rows)
                    note(path, f"L{i+1}: 1-col junk -> {len(new)} bullet(s)")
                else:
                    ncols = max(len(r) for r in rows)
                    new = rows_to_pipe(rows, header_rows)
                    note(path, f"L{i+1}: junk -> {ncols}-col pipe table ({len(rows)} rows, hdr={header_rows})")

                # drop trailing blank lines before region already in out
                while out and out[-1].strip() == "":
                    out.pop()
                # if we are inside an admonition body (last non-blank is a
                # field line or admonition header), indent the table body
                indent = ""
                k = len(out) - 1
                while k >= 0 and out[k].strip() == "":
                    k -= 1
                if k >= 0:
                    prev = out[k]
                    if ADMON_RE.match(prev) or prev.startswith("!!!"):
                        indent = "    "
                    elif FIELD_RE.match(prev) or (
                        prev.startswith("    ") and FIELD_RE.match(prev)
                    ):
                        indent = "    "
                    elif prev.startswith("    ") and not prev.strip().startswith("|"):
                        # inside admonition body already
                        indent = "    "

                for nl in new:
                    out.append((indent + nl) if indent else nl)
                # single blank line after
                out.append("")
                i = end
                continue

        out.append(lines[i])
        i += 1
    return out


def clean_field_lines(lines: list[str], lang: str, path: Path) -> list[str]:
    """Remove orphan Sphinx field lines; fold :class: kind into admonition."""
    mask = fence_mask(lines)
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        if mask[i]:
            out.append(ln)
            i += 1
            continue
        m = ADMON_RE.match(ln)
        if m:
            kind = m.group("kind")
            title = m.group("t") or ""
            header = m.group(1)
            j = i + 1
            body: list[str] = []
            while j < n:
                b = lines[j]
                if b.strip() == "":
                    k = j + 1
                    while k < n and lines[k].strip() == "":
                        k += 1
                    if k < n and (lines[k].startswith("    ") or lines[k].startswith("\t")):
                        body.append(b)
                        j += 1
                        continue
                    break
                if b.startswith("    ") or b.startswith("\t"):
                    body.append(b[4:] if b.startswith("    ") else b[1:])
                    j += 1
                    continue
                break
            kept: list[str] = []
            for b in body:
                if FIELD_RE.match(b):
                    mo = re.match(r"^[ \t]*:class:[ \t]*(\S+)", b)
                    if mo and mo.group(1).lower() in CLASS_KINDS:
                        newkind = mo.group(1).lower()
                        if newkind == "hint":
                            newkind = "tip"
                        if newkind in (
                            "tip", "warning", "info", "abstract", "success",
                            "question", "failure", "bug", "example", "quote",
                        ):
                            kind = newkind
                            note(path, f"L{i+1}: :class: {newkind} -> `!!! {newkind}`")
                        else:
                            note(path, f"L{i+1}: dropped orphan option `{b.strip()}`")
                    else:
                        note(path, f"L{i+1}: dropped orphan option `{b.strip()}`")
                    continue
                kept.append(b)
            while kept and kept[0].strip() == "":
                kept.pop(0)
            while kept and kept[-1].strip() == "":
                kept.pop()
            if kind != m.group("kind"):
                header = f"!!! {kind}"
            out.append(f'{header} "{title}"' if title else header)
            for b in kept:
                out.append(("    " + b) if b.strip() else "")
            i = j
            continue

        if FIELD_RE.match(ln):
            note(path, f"L{i+1}: dropped orphan option `{ln.strip()}`")
            i += 1
            continue

        out.append(ln)
        i += 1
    return out


def fix_math(lines: list[str], path: Path) -> list[str]:
    """(a) strip blank lines inside $$ blocks; (b) join multi-line inline $."""
    n = len(lines)
    mask = fence_mask(lines)
    out: list[str] = []
    i = 0
    changed_blank = changed_join = 0

    while i < n:
        if mask[i]:
            out.append(lines[i])
            i += 1
            continue

        s = lines[i].rstrip("\n")
        # ---- display math block
        if s.strip() == "$$" or (
            s.strip().startswith("$$") and not s.strip().endswith("$$")
        ) or (s.strip().startswith("$$") and s.strip().endswith("$$") and s.strip() != "$$" and len(s.strip()) > 2):
            # single-line $$...$$ display: leave (balanced already)
            if s.strip().startswith("$$") and s.strip().endswith("$$") and s.strip() != "$$" and len(s.strip()) > 4:
                out.append(s)
                i += 1
                continue
            # multi-line block starting with $$
            opener = s.strip()
            block = [s]
            i += 1
            closed = False
            while i < n and not mask[i]:
                t = lines[i].rstrip("\n")
                block.append(t)
                i += 1
                if t.strip() == "$$" or (t.strip().endswith("$$") and t.strip().startswith("$$") is False and t.strip() != ""):
                    if t.strip() == "$$" or t.strip().endswith("$$"):
                        closed = True
                        break
            # normalize: opener `$$` alone, closer `$$` alone, no blanks inside
            body = block[1:-1] if closed else block[1:]
            new_body = []
            for b in body:
                if b.strip() == "":
                    changed_blank += 1
                    continue
                new_body.append(b)
            out.append("$$")
            out.extend(new_body)
            if closed:
                out.append("$$")
            continue

        # ---- inline multi-line $...$
        t = re.sub(r"`[^`]*`", "", s)
        if "$$" not in t:
            dollars = re.findall(r"(?<!\\)\$", t)
            if len(dollars) % 2 == 1 and not s.strip().startswith("$$"):
                # join with following lines until balanced
                joined = s.rstrip()
                j = i + 1
                while j < n and not mask[j]:
                    nxt = lines[j].rstrip("\n")
                    if nxt.strip() == "" or nxt.strip().startswith("```"):
                        break
                    joined = joined.rstrip() + " " + nxt.strip()
                    j += 1
                    tt = re.sub(r"`[^`]*`", "", joined)
                    dd = re.findall(r"(?<!\\)\$", tt)
                    if len(dd) % 2 == 0:
                        break
                if j > i:
                    out.append(joined)
                    changed_join += 1
                    i = j
                    continue

        out.append(lines[i])
        i += 1

    if changed_blank:
        note(path, f"removed {changed_blank} blank line(s) inside $$ blocks")
    if changed_join:
        note(path, f"joined {changed_join} multi-line inline $ span(s)")
    return out


# ============================================================ sec: links
def pretty_sec_text(label: str) -> str:
    lab = label
    if lab.startswith("sec:"):
        lab = lab[4:]
    parts = lab.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else lab


def rel_link(from_rel: str, to_rel: str, label: str) -> str:
    """Relative md link from one contents/ file to another + anchor."""
    from pathlib import PurePosixPath
    src = PurePosixPath(from_rel).parent
    dst = PurePosixPath(to_rel)
    try:
        rel = PurePosixPath(dst).relative_to(src) if str(src) != "." else dst
    except ValueError:
        # walk up
        rel = None
    if rel is None or str(rel).startswith(".."):
        # compute manually
        up = 0
        a = list(src.parts)
        b = list(dst.parts)
        while a and b and a[0] == b[0]:
            a.pop(0)
            b.pop(0)
        up = len(a)
        rel = PurePosixPath(*([".."] * up + b))
    return f"{rel.as_posix()}#{label}"


def fix_sec_links(text: str, from_rel: str, path: Path) -> str:
    """Rewrite bare sec: link text and broken/cross-page sec: targets."""
    own_labels = {l for l, f in LABEL_MAP.items() if f == from_rel}
    stats = {"pretty": 0, "retarget": 0, "bare": 0}

    def repl(m: re.Match) -> str:
        text_part = m.group(1)
        hash_prefix = m.group(2) or ""
        label = m.group(3)
        trail = m.group(4) or ""
        if not label.startswith("sec:"):
            return m.group(0)
        stats["pretty"] += 1  # count all; adjusted below
        # target
        if label in own_labels:
            target = f"#{label}"
        elif label in LABEL_MAP:
            target = rel_link(from_rel, LABEL_MAP[label], label)
            stats["retarget"] += 1
        else:
            target = f"#{label}" if hash_prefix else f"#{label}"
        # text
        new_text = text_part
        if text_part.startswith("sec:") or text_part == label:
            new_text = pretty_sec_text(label)
            stats["bare"] += 1
        return f"[{new_text}]({target}{trail})"

    new = re.sub(
        r"\[([^\]]*)\]\((#?)(sec:[^)#\s]+)([^)]*)\)",
        repl,
        text,
    )
    # also handle [text](sec:xxx) with no hash already covered by (#?)
    if new != text:
        note(
            path,
            f"sec: links: {stats['bare']} pretty-text, {stats['retarget']} cross-page retargeted",
        )
    return new


# ============================================================ empty fences
def drop_empty_fences(lines: list[str], path: Path) -> list[str]:
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        m = FENCE_RE.match(lines[i])
        if m:
            j = i + 1
            body = []
            closed = False
            while j < n:
                if FENCE_RE.match(lines[j]) and lines[j].strip().endswith("`" * len(m.group(2))) and not lines[j].strip()[3:].strip():
                    closed = True
                    break
                body.append(lines[j])
                j += 1
            if closed and all(b.strip() == "" for b in body):
                note(path, f"L{i+1}: dropped empty fence")
                i = j + 1
                continue
        out.append(lines[i])
        i += 1
    return out


# ============================================================ main
def process_file(fn: str, lang: str) -> None:
    path = ROOT / lang / EE / fn
    if not path.exists():
        print(f"MISSING {path}")
        return
    from_rel = f"{EE.split('contents/')[1]}/{fn}" if "contents/" in EE else fn
    from_rel = f"essentialelements/{fn}"

    orig = path.read_text(encoding="utf-8")
    lines = orig.split("\n")

    lines = drop_empty_fences(lines, path)
    lines = replace_tables_from_source(lines, lang, fn, path)
    lines = fix_myst_fences(lines, path)
    lines = clean_field_lines(lines, lang, path)
    lines = fix_math(lines, path)

    text = "\n".join(lines)
    text = strip_span_roles_text(text)
    text = fix_sec_links(text, from_rel, path)

    # tidy: collapse 3+ blank lines to 2, strip trailing spaces on non-code
    lines = text.split("\n")
    mask = fence_mask(lines)
    cleaned = []
    blanks = 0
    for i, ln in enumerate(lines):
        if not mask[i]:
            ln = ln.rstrip()
        if ln.strip() == "":
            blanks += 1
            if blanks > 2:
                continue
        else:
            blanks = 0
        cleaned.append(ln)
    text = "\n".join(cleaned)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        note(path, "updated")
    else:
        note(path, "no change")


def main() -> None:
    global LABEL_MAP
    LABEL_MAP = json.loads(Path("/tmp/ee_label_map.json").read_text())
    only = sys.argv[1:] or None
    for lang in ("en", "zh"):
        for fn in FILES:
            if only and fn not in only and f"{lang}/{fn}" not in only:
                continue
            process_file(fn, lang)
    for p, msgs in sorted(report.items()):
        if msgs == ["no change"]:
            print(f"{p}: no change")
        else:
            print(f"{p}:")
            for m in msgs:
                print(f"  - {m}")


if __name__ == "__main__":
    main()
