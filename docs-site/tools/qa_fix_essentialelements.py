#!/usr/bin/env python3
"""QA-fix essentialelements manual markdown for MkDocs rendering.

Fixes in docs/{en,zh}/manual/contents/essentialelements/{9 target files}:
  1. LaTeX table-size wrappers `!!! note "latex"` / `!!! note "\\Y{...}"` -> dropped.
  2. Orphan Sphinx field lines (:class: :header-rows: :width: ... :option:) -> removed;
     `:class: tip|warning|info` folds into the admonition type.
  3. MyST list-table bodies (`* -` rows) inside `!!! note` -> Markdown pipe tables,
     matching the existing house style in output.md (note caption + pipe table).
     One-column list-tables become bullet lists.
  4. Leftover table-span roles {cspan}`N` / {rspan}`N` -> stripped (text kept),
     same rule as qa_fix_manual.py. Short rows are padded.
  5. MyST targets `(name)=` -> `<a id="name"></a>`.
  6. Image paths -> ../../../images/manual/NAME (unresolved/wildcard dropped).
  7. Broken fences (unclosed EOF fence, `` ``` --> `` tails) repaired.

Keeps code block bodies, ORCA keywords, and <a id=...> labels. Does not translate.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs")
FILES = [
    "index_essentialelements.md",
    "input.md",
    "coordinates.md",
    "basics.md",
    "output.md",
    "parallel.md",
    "scf.md",
    "initialguess.md",
    "basisset.md",
]

# same field list as tools/qa_fix_manual.py
FIELD_RE = re.compile(
    r"^[ \t]*:(?:width|class|header-rows|subcaptions|class-grid|align|scale"
    r"|name|alt|figwidth|figclass|option):[^\n]*$"
)
SPAN_ROLE_RE = re.compile(r"\{(?:cspan|rspan)\}`[^`]*`")
IMG_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)")
FENCE_RE = re.compile(r"^([ \t]*)(`{3,})(.*)$")
LABEL_TARGET_RE = re.compile(r"^\(([A-Za-z0-9_:.+/-]+)\)[ \t]*=[ \t]*$", re.M)
ADMON_RE = re.compile(
    r'^(!!!\s+(?P<kind>note|tip|warning|info|abstract|success|question|failure|bug|example|quote))'
    r'(?P<title>\s+"(?P<t>[^"]*)")?[ \t]*$'
)
CELL_START_RE = re.compile(r"^(\s*)\* -(?: (.*))?$")
CELL_CONT_RE = re.compile(r"^(\s*)-(?: (.*))?$")
YWIDTH_RE = re.compile(r"^\\Y\{")

report: dict[str, list[str]] = {}


def note(path: Path, msg: str) -> None:
    report.setdefault(str(path), []).append(msg)


# ---------------------------------------------------------------- images
def resolve_image(lang: str, name: str) -> str | None:
    manual = ROOT / lang / "images" / "manual"
    if not name:
        return None
    if "*" not in name:
        cand = manual / name
        return name if cand.exists() else None
    stem = name.split("*")[0]
    if not stem or not manual.exists():
        return None
    matches = sorted(
        p.name for p in manual.iterdir() if p.is_file() and p.name.startswith(stem)
    )
    exact = [m for m in matches if m[len(stem) :].count(".") == 1]
    return exact[0] if exact else (matches[0] if matches else None)


def fix_inline_images(text: str, lang: str) -> str:
    def repl(m: re.Match) -> str:
        alt, path = m.group("alt"), m.group("path")
        if path.startswith("http"):
            return m.group(0)
        fname = path.split("/")[-1]
        resolved = resolve_image(lang, fname)
        if resolved is None:
            return m.group(0)
        return f"![{alt}](../../../images/manual/{resolved})"

    return IMG_RE.sub(repl, text)


# ---------------------------------------------------------------- fences
def is_in_fence(lines: list[str], idx: int) -> bool:
    stack: list[tuple[int, int, str]] = []
    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if m:
            marker, rest = m.group(2), m.group(3).strip()
            if not stack:
                stack.append((i, len(marker), rest))
            else:
                _oi, om, _orest = stack[-1]
                if rest == "" and marker[0] == "`" and len(marker) >= om:
                    stack.pop()
                else:
                    stack.append((i, len(marker), rest))
        if i == idx:
            return bool(stack)
    return False


def fix_broken_fences(text: str, path: Path) -> str:
    lines = text.split("\n")
    changed = 0
    glued_arrow = False
    for i, ln in enumerate(lines):
        m = FENCE_RE.match(ln)
        if m and "-->" in ln and m.group(3).strip().startswith("-->"):
            lines[i] = re.sub(r"(`{3,})[ \t]*-->[ \t]*$", r"\1", ln)
            changed += 1
            glued_arrow = True
            note(str(path), f"broken fence closer L{i+1}: stripped trailing '-->'")
    text2 = "\n".join(lines)

    if glued_arrow:
        openers = [i for i, ln in enumerate(lines) if "<!--" in ln and "-->" not in ln]
        if openers:
            oi = openers[-1]
            lines[oi] = lines[oi].replace("<!--", "", 1)
            if lines[oi].strip() == "":
                del lines[oi]
            changed += 1
            note(str(path), f"uncommented block opened at L{oi+1}")
            text2 = "\n".join(lines)

    lines = text2.split("\n")
    stack: list[tuple[int, int, str]] = []
    for i, ln in enumerate(lines):
        m = FENCE_RE.match(ln)
        if not m:
            continue
        marker, rest = m.group(2), m.group(3).strip()
        if not stack:
            stack.append((i, len(marker), rest))
        else:
            _oi, om, _orest = stack[-1]
            if rest == "" and marker[0] == "`" and len(marker) >= om:
                stack.pop()
            else:
                stack.append((i, len(marker), rest))
    if stack:
        oi, om, _orest = stack[-1]
        end = len(lines)
        while end > oi + 1 and lines[end - 1].strip() == "":
            end -= 1
        lines.insert(end, "`" * om)
        changed += 1
        note(str(path), f"unclosed fence from L{oi+1} closed at L{end+1}")
        text2 = "\n".join(lines)

    return text2 if changed else text


# ---------------------------------------------------------------- labels / roles
def fix_labels(text: str, path: Path) -> str:
    def repl(m: re.Match) -> str:
        note(str(path), f"MyST target ({m.group(1)})= -> <a id>")
        return f'<a id="{m.group(1)}"></a>'

    return LABEL_TARGET_RE.sub(repl, text)


def fix_roles(text: str, path: Path) -> str:
    """Strip any leftover inline MyST roles of the kinds named in the brief."""
    before = text

    def ref(m: re.Match) -> str:
        inner = m.group(1)
        if "<" in inner and inner.endswith(">"):
            t, _, lab = inner.rpartition("<")
            return f"[{t.strip()}](#{lab[:-1].strip()})"
        return f"[{inner}](#{inner})"

    text = re.sub(r"\{ref\}`([^`]+)`", ref, text)
    text = re.sub(r"\{numref\}`([^`]+)`", ref, text)
    text = re.sub(r"\{cite\}`([^`]+)`", lambda m: f"[{m.group(1)}](../../bibliography.md)", text)
    text = re.sub(r"\{eq\}`([^`]+)`", lambda m: f"[Eq](#{m.group(1)})", text)
    text = re.sub(r"\{index\}`[^`]*`", "", text)
    text = re.sub(r"\{download\}`([^`]+)`", r"`\1`", text)
    if text != before:
        note(str(path), "stripped leftover MyST roles")
    return text


def fix_span_roles(text: str, path: Path) -> str:
    new = SPAN_ROLE_RE.sub("", text)
    if new != text:
        n = len(SPAN_ROLE_RE.findall(text))
        note(str(path), f"stripped {n} cspan/rspan role(s)")
    return new


# ---------------------------------------------------------------- list-tables
RSPAN_RE = re.compile(r"^\{rspan\}`(\d+)`\s*(.*)$")
CSPAN_RE = re.compile(r"^\{cspan\}`\d+`\s*(.*)$")


def join_cell_lines(lines: list[str]) -> str:
    if not lines:
        return ""
    text = lines[0]
    for ln in lines[1:]:
        if text.endswith("\\"):
            text = text[:-1].rstrip() + "<br>"
        else:
            text = text.rstrip() + " "
        text += ln
    text = text.strip()
    if text.endswith("<br>"):
        text = text[:-4].rstrip()
    return text


def parse_list_table(body: list[str]) -> list[list[str]]:
    """Parse `* -` / `- ` list-table rows into a list of cell-lists."""
    rows: list[list[str]] = []
    cur_row: list[str] = []
    cur: list[str] = []
    cell_indent: int | None = None
    in_row = False

    def flush_cell() -> None:
        nonlocal cur
        if in_row:
            cur_row.append(join_cell_lines(cur))
        cur = []

    def flush_row() -> None:
        nonlocal cur_row, in_row
        if not in_row:
            return
        flush_cell()
        if cur_row:
            rows.append(cur_row)
        cur_row = []
        in_row = False

    for ln in body:
        if ln.strip() == "":
            continue
        m = CELL_START_RE.match(ln)
        if m:
            flush_row()
            cell_indent = len(m.group(1)) + 2
            cur = [m.group(2) or ""]
            in_row = True
            continue
        m = CELL_CONT_RE.match(ln)
        if m and cell_indent is not None and len(m.group(1)) == cell_indent:
            flush_cell()
            cur = [m.group(2) or ""]
            continue
        cur.append(ln.strip())
    flush_row()
    return rows


def expand_grid(rows: list[list[str]]) -> tuple[list[list[str]], int]:
    """Expand list-table rows (with rspan/cspan roles) into a rectangular grid.

    `{rspan}`N` text` covers the next N rows in that column.
    `{cspan}`N` text` is a full-width section header row.
    Returns (grid, ncols).
    """
    # first pass: how many columns?
    ncols = 0
    for row in rows:
        if len(row) == 1 and CSPAN_RE.match(row[0].strip()):
            continue
        # a row with an rspan cell omits that column in following rows,
        # so raw cell count is only a lower bound for the first row
        ncols = max(ncols, len(row))
    if ncols == 0:
        return [], 0

    grid: list[list[str]] = []
    skip = [0] * ncols  # rows remaining that each column is covered by an rspan
    for row in rows:
        stripped = [c.strip() for c in row]
        if len(row) == 1 and CSPAN_RE.match(stripped[0]):
            text = CSPAN_RE.match(stripped[0]).group(1).strip()
            # section-header row: bold, but don't stack on existing emphasis
            if re.fullmatch(r"\*[^*]+\*", text):
                text = "**" + text[1:-1] + "**"
            elif not text.startswith("*"):
                text = "**" + text + "**"
            grid.append([text] + [""] * (ncols - 1))
            skip = [0] * ncols
            continue
        out = [""] * ncols
        it = iter(stripped)
        for c in range(ncols):
            if skip[c] > 0:
                skip[c] -= 1
                continue
            cell = next(it, "")
            m = RSPAN_RE.match(cell)
            if m:
                out[c] = m.group(2).strip()
                skip[c] = int(m.group(1))
            else:
                out[c] = cell
        grid.append(out)
    return grid, ncols


def table_to_pipe(grid: list[list[str]], ncols: int) -> list[str]:
    def esc(cell: str) -> str:
        return cell.replace("|", "\\|").strip()

    out = ["| " + " | ".join(esc(c) for c in grid[0]) + " |"]
    out.append("| " + " | ".join("---" for _ in range(ncols)) + " |")
    for r in grid[1:]:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return out


def is_list_table(body: list[str]) -> bool:
    """True if body is a MyST list-table (every non-blank line fits the grammar)."""
    content = [ln for ln in body if ln.strip() and not FIELD_RE.match(ln)]
    if not content:
        return False
    row_indent: int | None = None
    cell_indent: int | None = None
    saw_row = False
    for ln in content:
        if CELL_START_RE.match(ln):
            row_indent = len(CELL_START_RE.match(ln).group(1))
            cell_indent = row_indent + 2
            saw_row = True
            continue
        m = CELL_CONT_RE.match(ln)
        if m and cell_indent is not None and len(m.group(1)) == cell_indent:
            continue
        # deeper-indent cell continuation
        indent = len(ln) - len(ln.lstrip())
        if cell_indent is not None and indent > cell_indent:
            continue
        return False
    return saw_row


def convert_list_table_body(body: list[str], path: Path) -> list[str]:
    rows = parse_list_table([ln for ln in body if ln.strip() and not FIELD_RE.match(ln)])
    grid, ncols = expand_grid(rows)
    if ncols <= 1:
        bullets = [f"* {r[0].strip()}" for r in rows if r and r[0].strip()]
        note(str(path), f"list-table -> {len(bullets)} bullet(s)")
        return bullets
    pipe = table_to_pipe(grid, ncols)
    note(str(path), f"list-table -> {ncols}-column pipe table ({len(rows)} rows)")
    return pipe


# ---------------------------------------------------------------- admonitions
def process_admonitions(text: str, path: Path) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        m = ADMON_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue

        kind = m.group("kind")
        title = m.group("t") or ""
        header = m.group(1)
        j = i + 1
        body: list[str] = []
        while j < n:
            ln = lines[j]
            if ln.strip() == "":
                k = j + 1
                while k < n and lines[k].strip() == "":
                    k += 1
                if k < n and (lines[k].startswith("    ") or lines[k].startswith("\t")):
                    body.append(ln)
                    j += 1
                    continue
                break
            if ln.startswith("    ") or ln.startswith("\t"):
                body.append(ln[4:] if ln.startswith("    ") else ln[1:])
                j += 1
                continue
            break
        while body and body[-1].strip() == "":
            body.pop()
            j -= 1

        # 1) LaTeX size wrappers -> drop whole block
        if title.strip() == "latex":
            note(str(path), f"L{i+1}: dropped `!!! note \"latex\"` wrapper")
            i = j
            continue
        if YWIDTH_RE.match(title.strip()):
            note(str(path), f"L{i+1}: dropped `!!! note \"\\\\Y{{...}}\"` column-width marker")
            i = j
            continue

        # 2) orphan field lines; fold :class: tip|warning|info into kind
        kept: list[str] = []
        for ln in body:
            if FIELD_RE.match(ln):
                mo = re.match(r"^[ \t]*:class:[ \t]*(\S+)", ln)
                if mo and mo.group(1) in (
                    "tip", "warning", "info", "abstract", "success",
                    "question", "failure", "bug", "example", "quote",
                ):
                    kind = mo.group(1)
                    note(str(path), f"L{i+1}: :class: {kind} -> `!!! {kind}`")
                else:
                    note(str(path), f"L{i+1}: dropped orphan option `{ln.strip()}`")
                continue
            kept.append(ln)
        while kept and kept[0].strip() == "":
            kept.pop(0)
        while kept and kept[-1].strip() == "":
            kept.pop()

        # 3) list-table body -> pipe table / bullets
        if is_list_table(kept):
            kept = convert_list_table_body(kept, path)

        # rebuild
        if kind != m.group("kind"):
            header = f"!!! {kind}"
        out.append(f'{header} "{title}"' if title else header)
        for ln in kept:
            out.append(("    " + ln) if ln.strip() else "")
        i = j

    return "\n".join(out)


# ---------------------------------------------------------------- glue
def process_file(path: Path, lang: str) -> None:
    orig = path.read_text(encoding="utf-8")
    text = orig
    text = fix_broken_fences(text, path)
    text = fix_labels(text, path)
    text = fix_roles(text, path)
    text = process_admonitions(text, path)
    text = fix_span_roles(text, path)
    text = fix_inline_images(text, lang)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        note(str(path), "updated")
    else:
        note(str(path), "no change")


def main() -> None:
    for lang in ("en", "zh"):
        for fn in FILES:
            p = ROOT / lang / "manual" / "contents" / "essentialelements" / fn
            if not p.exists():
                print(f"MISSING {p}")
                continue
            process_file(p, lang)
    for path, msgs in sorted(report.items()):
        if msgs != ["no change"]:
            print(f"{path}:")
            for msg in msgs:
                print(f"  - {msg}")
        else:
            print(f"{path}: no change")


if __name__ == "__main__":
    main()
