#!/usr/bin/env python3
"""QA-fix modelchemistries Manual markdown for MkDocs rendering.

Fixes in docs/{en,zh}/manual/contents/modelchemistries/*.md:
  1. MyST flat/list-table residue (`| Item | Value |` stubs, `* -` rows,
     indented `-` cells, orphan `:class:`/`:header-rows:` lines) -> proper
     Markdown pipe tables inside `!!! note "caption"`, rebuilt from the
     ORIGINAL MyST source (md/manual/{en,zh}) with {cspan}/{rspan} expanded
     to empty continuation cells.
  2. Leftover MyST directive fences ```{note}/{attention}/{tip} -> Material
     admonitions; ```{bibliography} blocks -> bullet list of bibliography
     links (same convention as inline [key](../../bibliography.md) cites).
  3. Orphan Sphinx field lines outside fences -> removed; leftover
     {cspan}/{rspan} roles -> stripped.
  4. Math hygiene (pymdownx.arithmatex rules): remove blank lines inside
     `$$...$$` display blocks (they silently disable math), strip trailing
     whitespace on `$$` delimiter lines, fix inline `$...$` closers preceded
     by whitespace, join multi-line inline `$...$` spans, drop dead
     `<!--$$ ... $$-->` alternative-equation comments.
  5. Equation labels: insert `<a id="LABEL"></a>` before display math that
     carries `\\qquad \\text{(LABEL)}` so prose `[Eq](#LABEL)` refs resolve.
  6. bare `sec:` in prose -> `[shortname](#sec:...)` links; link text of
     `[sec:...](#sec:...)` -> last two id segments.
  7. Image paths -> ../../../images/manual/NAME.ext (wildcards like `71.*`
     resolved against the asset directory).

Never touches fenced code bodies (ORCA inputs/outputs). Does not translate.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca")
MYSQ = {"en": ROOT / "md/manual/en", "zh": ROOT / "md/manual/zh"}
DOCS = ROOT / "docs-site/docs"

CHAPTER = "manual/contents/modelchemistries"
# MyST sources live at md/manual/{lang}/contents/modelchemistries (no "manual/" prefix)
CHAPTER_MYST = "contents/modelchemistries"

ADMON_MAP = {
    "note": "note", "warning": "warning", "important": "warning",
    "tip": "tip", "hint": "tip", "attention": "warning",
    "caution": "warning", "seealso": "info", "deprecated": "warning",
}

FIELD_RE = re.compile(
    r"^[ \t]*:(?:width|class|header-rows|subcaptions|class-grid|align|scale"
    r"|name|alt|figwidth|figclass|option|stub-columns|widths|alignments"
    r"|language|path|caption|linenos|dedent|encoding|tab-width|start-after"
    r"|end-before|emphasize-lines|lines|nofigentry|list|filter|depth"
    r"|maxdepth|glob|reversed|numbered):[^\n]*$"
)
SPAN_ROLE_RE = re.compile(r"\{(?:cspan|rspan)\}`[^`]*`")
FENCE_RE = re.compile(r"^([ \t]*)(`{3,})(.*)$")
IMG_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)")

NOTE_START_RE = re.compile(
    r'^(?P<indent>[ \t]*)!!! (?P<kind>\w+)(?P<title> "[^"]*")?[ \t]*$'
)

STUB_HEAD_RE = re.compile(r"^\| (?:Item \| Value|项目 \| 内容) \|$")
STUB_SEP_RE = re.compile(r"^\|[\s:|-]+\|$")
STUB_ROW_RE = re.compile(r"^\| .+ \| (?:—|无|–) \|$")
CELL_LINE_RE = re.compile(r"^ {4,}- ?\S?.*$")
STAR_LINE_RE = re.compile(r"^\s+\* -(?: .*)?$")
INLINE_SPAN_START = re.compile(r"(?<!\\)\$(?!\s)")


def fence_mask(lines: list[str]) -> set[int]:
    """Indices of lines inside (or forming) fenced code blocks."""
    res: set[int] = set()
    open_ = False
    for i, ln in enumerate(lines):
        if FENCE_RE.match(ln):
            res.add(i)
            open_ = not open_
            continue
        if open_:
            res.add(i)
    return res


def esc_pipe(text: str) -> str:
    return text.replace("|", "\\|")


# ============================================================ 1. tables
SPAN_RE = re.compile(r"\{([cr])span\}`(\d+)`")


def strip_spans(text: str) -> tuple[str, int, int]:
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


def parse_rows(body: str) -> list[list[tuple[str, int, int]]]:
    rows: list[list[tuple[str, int, int]]] = []
    for line in body.splitlines():
        if not line.strip():
            continue
        m_row = re.match(r"^\s*\* -[ \t]*(.*)$", line)
        if m_row:
            content, cs, rs = strip_spans(m_row.group(1))
            rows.append([(content, cs, rs)])
            continue
        m_cell = re.match(r"^[ \t]+-[ \t]*(.*)$", line)
        if m_cell and rows:
            content, cs, rs = strip_spans(m_cell.group(1))
            rows[-1].append((content, cs, rs))
    return rows


def build_grid(rows: list[list[tuple[str, int, int]]]) -> list[list[str]]:
    ncols = max((sum(cs for _, cs, _ in r) for r in rows), default=0)
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
                        grid[rj][cj] = text if (dr == 0 and dc == 0) else ""
            ci += cs
    return [[c if c is not None else "" for c in row] for row in grid]


def grid_to_pipe(grid: list[list[str]], header_rows: int) -> str:
    if not grid:
        return ""
    ncols = len(grid[0])
    lines: list[str] = []
    start = 0
    if header_rows > 0:
        for r in range(header_rows):
            lines.append("| " + " | ".join(esc_pipe(c) for c in grid[r]) + " |")
        start = header_rows
    else:
        lines.append("| " + " | ".join([""] * ncols) + " |")
    lines.append("|" + "---|" * ncols)
    for r in range(start, len(grid)):
        lines.append("| " + " | ".join(esc_pipe(c) for c in grid[r]) + " |")
    return "\n".join(lines)


DIRECTIVE_RE = re.compile(
    r"^:::\{(?P<kind>flat-table|list-table)\}[ \t]*(?P<title>[^\n]*)\n"
    r"(?P<body>.*?)^:::[ \t]*$",
    re.M | re.S,
)


def extract_myst_tables(text: str) -> list[dict]:
    tables = []
    for m in DIRECTIVE_RE.finditer(text):
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
        rows = parse_rows(cell_body)
        if not rows:
            continue
        tables.append({
            "title": title,
            "header_rows": header_rows,
            "grid": build_grid(rows),
        })
    return tables


def is_residue_line(ln: str) -> str | None:
    s = ln.rstrip()
    if s.strip() == "":
        return "blank"
    if FIELD_RE.match(s):
        return "opt"
    if STUB_HEAD_RE.match(s):
        return "stub"
    if STUB_SEP_RE.match(s):
        return "sep"
    if STUB_ROW_RE.match(s):
        return "stubrow"
    if STAR_LINE_RE.match(s):
        return "star"
    if CELL_LINE_RE.match(s):
        return "cell"
    return None


def find_broken_note_regions(text: str) -> list[tuple[int, int, str]]:
    """Regions [start, end) beginning at `!!! note ...` followed by residue."""
    lines = text.split("\n")
    regions: list[tuple[int, int, str]] = []
    i = 0
    while i < len(lines):
        m = NOTE_START_RE.match(lines[i])
        if not m or m.group("indent"):
            i += 1
            continue
        title = m.group("title") or ""
        title = title.strip().lstrip('"').rstrip('"').strip()
        j = i + 1
        saw_residue = False
        while j < len(lines):
            kind = is_residue_line(lines[j])
            if kind is None:
                break
            if kind in ("stub", "star", "stubrow"):
                saw_residue = True
            if kind == "blank":
                k = j + 1
                while k < len(lines) and is_residue_line(lines[k]) == "blank":
                    k += 1
                if k < len(lines) and is_residue_line(lines[k]) in (
                    "opt", "stub", "sep", "stubrow", "star", "cell"
                ):
                    j += 1
                    continue
                break
            j += 1
        if saw_residue:
            regions.append((i, j, title))
        i = j if j > i else i + 1
    return regions


def norm_title(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip().rstrip(".").strip("`").strip()


def fix_tables(text: str, myst_text: str) -> tuple[str, int, list[str]]:
    notes: list[str] = []
    tables = extract_myst_tables(myst_text)
    regions = find_broken_note_regions(text)
    if not regions:
        return text, 0, notes

    # match by title first, then by order for leftovers
    used: set[int] = set()
    pairs: list[tuple[tuple[int, int, str], dict | None]] = []
    for reg in regions:
        rtitle = norm_title(reg[2])
        hit = None
        for ti, t in enumerate(tables):
            if ti in used:
                continue
            if norm_title(t["title"]) == rtitle:
                hit = t
                used.add(ti)
                break
        pairs.append((reg, hit))
    leftover = [t for ti, t in enumerate(tables) if ti not in used]
    li = 0
    for idx, (reg, t) in enumerate(pairs):
        if t is None and li < len(leftover):
            pairs[idx] = (reg, leftover[li])
            li += 1

    lines = text.split("\n")
    changed = 0
    for (start, end, title), t in reversed(pairs):
        if t is None:
            notes.append(f"    ! no MyST table for note {title!r} (left as-is)")
            continue
        hr = t["header_rows"] or 1
        content = grid_to_pipe(t["grid"], hr)
        cap = t["title"].strip() or title
        indented = "\n".join(
            ("    " + ln) if ln.strip() else "" for ln in content.splitlines()
        )
        repl = f'!!! note "{cap}"\n{indented}\n'
        lines[start:end] = repl.split("\n")
        changed += 1
        notes.append(f"    table rebuilt: {cap!r} ({len(t['grid'])} rows)")
    return "\n".join(lines), changed, notes


# ==================================================== 2. MyST directive fences
MYST_FENCE_RE = re.compile(r"^```(?P<type>[a-zA-Z-]+)(?P<title>[^\n]*)$")


def fix_myst_fences(text: str) -> tuple[str, int, list[str]]:
    lines = text.split("\n")
    out: list[str] = []
    notes: list[str] = []
    changed = 0
    i = 0
    while i < len(lines):
        m = MYST_FENCE_RE.match(lines[i])
        if not m or m.group("type") in ("", "orca", "orcainput", "text", "console",
                                        "python", "mol", "powershell", "bash", "json"):
            out.append(lines[i])
            i += 1
            continue
        typ = m.group("type")
        # gather body until closing fence
        j = i + 1
        body: list[str] = []
        while j < len(lines) and not re.match(r"^```\s*$", lines[j]):
            body.append(lines[j])
            j += 1
        closer = j < len(lines)
        if typ in ("note", "attention", "tip", "warning", "important", "caution",
                   "hint", "seealso", "deprecated"):
            kind = ADMON_MAP.get(typ, "note")
            title = m.group("title").strip()
            indented = "\n".join(
                ("    " + ln) if ln.strip() else "" for ln in body
            )
            head = f"!!! {kind}" + (f" {title}" if title else "")
            out.append(head)
            out.extend(indented.split("\n") if indented else [])
            out.append("")
            changed += 1
            notes.append(f"    fence ```{{{typ}}}-> !!! {kind} ({len(body)} lines)")
        elif typ == "bibliography":
            keys = [ln.strip() for ln in body
                    if ln.strip() and not ln.strip().startswith(":")]
            out.append("")
            for k in keys:
                out.append(f"-   [{k}](../../bibliography.md)")
            out.append("")
            changed += 1
            notes.append(f"    fence ```{{bibliography}} -> {len(keys)} cite links")
        else:
            # unknown MyST directive fence: keep as-is but report
            out.append(lines[i])
            out.extend(body)
            notes.append(f"    ! unhandled MyST fence ```{{{typ}}} at L{i+1}")
        i = j + 1 if closer else j
    return "\n".join(out), changed, notes


# ============================================ 3. orphan fields / span roles
def fix_field_lines(text: str) -> tuple[str, int]:
    lines = text.split("\n")
    fence = fence_mask(lines)
    out = []
    changed = 0
    for i, ln in enumerate(lines):
        if FIELD_RE.match(ln) and i not in fence:
            changed += 1
            continue
        out.append(ln)
    return "\n".join(out), changed


def fix_span_roles(text: str, myst: bool = True) -> tuple[str, int]:
    if not myst:
        return text, 0
    new, n = SPAN_ROLE_RE.subn("", text)
    return new, n


# ================================================================ 4. math
def fix_math(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    lines = text.split("\n")
    fence = fence_mask(lines)

    # (a) drop dead <!--$$ ... $$--> alternative-equation comment blocks
    out: list[str] = []
    i = 0
    dropped = 0
    while i < len(lines):
        if i not in fence and lines[i].rstrip() == "<!--$$":
            j = i + 1
            while j < len(lines) and lines[j].rstrip() != "$$-->":
                j += 1
            if j < len(lines):
                dropped += 1
                i = j + 1
                continue
        out.append(lines[i])
        i += 1
    if dropped:
        notes.append(f"    dropped {dropped} dead <!--$$ ... $$--> blocks")
    lines = out

    # (b) normalize $$ delimiter lines (strip trailing whitespace) and
    #     remove blank lines inside display blocks
    fence = fence_mask(lines)
    out = []
    i = 0
    trimmed = 0
    unblanked = 0
    while i < len(lines):
        ln = lines[i]
        if i not in fence and ln.rstrip() == "$$":
            if ln != "$$":
                trimmed += 1
            out.append("$$")
            i += 1
            # body until closer
            body: list[str] = []
            while i < len(lines):
                b = lines[i]
                if b.rstrip() == "$$":
                    if b != "$$":
                        trimmed += 1
                    break
                body.append(b)
                i += 1
            stripped = [b for b in body if b.strip() != ""]
            if len(stripped) != len(body):
                unblanked += 1
            out.extend(stripped)
            if i < len(lines):
                out.append("$$")
                i += 1
            continue
        out.append(ln)
        i += 1
    if trimmed:
        notes.append(f"    trimmed trailing ws on {trimmed} $$ delimiter lines")
    if unblanked:
        notes.append(f"    removed blank lines inside {unblanked} $$ blocks")
    lines = out

    # (c)+(d) join multi-line inline spans; fix whitespace-before-closer
    fence = fence_mask(lines)

    def unpaired(line: str) -> str:
        """Remove valid inline spans; return what's left."""
        t = re.sub(
            r"(?<!\\)\$(?!\s)((?:\\.|[^\\$])+?)(?<!\s)\$", "", line
        )
        return t.replace("\\$", "")

    joined = 0
    fixed_close = 0
    i = 0
    while i < len(lines) - 1:
        if i in fence or (i + 1) in fence:
            i += 1
            continue
        a, b = lines[i], lines[i + 1]
        if a.strip() and b.strip() and unpaired(a).count("$") % 2 == 1:
            cand = a.rstrip() + b.lstrip()
            if unpaired(cand).count("$") == 0:
                lines[i] = cand
                del lines[i + 1]
                joined += 1
                continue
        i += 1
    if joined:
        notes.append(f"    joined {joined} multi-line inline $..$ spans")
    text = "\n".join(lines)

    # whitespace immediately before an inline closing $ : "... > $ x" -> "... >$ x"
    # only rewrite whole spans so spaces before *opening* dollars survive
    lines = text.split("\n")
    fence = fence_mask(lines)
    in_dd = False
    SPAN_FIX_RE = re.compile(
        r"(?<!\\)\$(?!\s)((?:\\.|[^\\$])+?)\s+\$"
    )
    for i, ln in enumerate(lines):
        if i in fence:
            continue
        if ln.rstrip() == "$$":
            in_dd = not in_dd
            continue
        if in_dd:
            continue
        new, n = SPAN_FIX_RE.subn(lambda m: f"${m.group(1)}$", ln)
        if n:
            lines[i] = new
            fixed_close += n
    if fixed_close:
        notes.append(f"    fixed whitespace-before-closer on {fixed_close} inline $ lines")
    return "\n".join(lines), notes


# ============================================================ 5. eq anchors
EQ_LABEL_RE = re.compile(r"\\qquad \\text\{\(([^)]+)\)\}")


def fix_eq_anchors(text: str) -> tuple[str, int, list[str]]:
    notes: list[str] = []
    lines = text.split("\n")
    fence = fence_mask(lines)
    existing = set(re.findall(r'<a id="([^"]+)"></a>', text))
    out: list[str] = []
    added = 0
    i = 0
    while i < len(lines):
        ln = lines[i]
        if i not in fence and ln.rstrip() == "$$":
            # look ahead over body for a label
            body: list[str] = []
            j = i + 1
            while j < len(lines) and lines[j].rstrip() != "$$":
                body.append(lines[j])
                j += 1
            label = None
            for b in body:
                m = EQ_LABEL_RE.search(b)
                if m:
                    label = m.group(1).strip()
                    break
            if label:
                # choose id that prose refs actually use
                target_ids = [label]
                if ":" in label and label.split(":", 1)[0] in ("eq", "eqn"):
                    target_ids += [label.split(":", 1)[1]]
                else:
                    target_ids += [f"eq:{label}", f"eqn:{label}"]
                chosen = None
                for cand in target_ids:
                    if re.search(rf"\]\(#{re.escape(cand)}\)", text) or (
                        f'id="{cand}"' in existing
                    ):
                        chosen = cand
                        break
                if chosen is None:
                    chosen = label if label.startswith("eq") else f"eq:{label}"
                aid = f'<a id="{chosen}"></a>'
                if aid not in existing and f'id="{chosen}"' not in "\n".join(out[-3:]):
                    # avoid duplicate anchors
                    already = any(
                        re.match(rf'^<a id="{re.escape(chosen)}"></a>$', o)
                        for o in out[-5:]
                    )
                    if not already:
                        out.append(aid)
                        out.append("")
                        added += 1
                        existing.add(chosen)
            out.append("$$")
            out.extend(body)
            if j < len(lines):
                out.append("$$")
            i = j + 1
            continue
        out.append(ln)
        i += 1
    if added:
        notes.append(f"    added {added} <a id=eqn:...> anchors")
    return "\n".join(out), added, notes


# ============================================================ 6. sec: refs
def pretty_sec_text(secid: str) -> str:
    parts = secid.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else secid


def fix_sec_refs(text: str) -> tuple[str, int, int, list[str]]:
    notes: list[str] = []
    lines = text.split("\n")
    fence = fence_mask(lines)
    wrapped = 0
    pretty = 0
    for i, ln in enumerate(lines):
        if i in fence:
            continue
        # skip anchors and raw html
        work = ln
        # 1) pretty link text for [sec:a.b.c](#sec:a.b.c)
        def prettify(m: re.Match) -> str:
            nonlocal pretty
            txt, tgt = m.group(1), m.group(2)
            if txt.startswith("sec:") and "#sec:" in tgt:
                short = pretty_sec_text(txt[4:])
                pretty += 1
                return f"[{short}]({tgt})"
            return m.group(0)

        work = re.sub(r"\[([^\]]*)\]\((#[^)]*)\)", prettify, work)

        # 2) wrap truly bare sec: tokens in prose
        def wrap(m: re.Match) -> str:
            nonlocal wrapped
            secid = m.group(1)
            short = pretty_sec_text(secid)
            wrapped += 1
            return f"[{short}](#{secid})"

        # remove anchors, links, code spans before detecting bare tokens
        probe = re.sub(r"<a id=\"[^\"]*\"></a>", "", work)
        probe = re.sub(r"\[[^\]]*\]\([^)]*\)", "", probe)
        probe = re.sub(r"`[^`]*`", "", probe)
        if re.search(r"(?<![\w\"'(])sec:[A-Za-z0-9._]+", probe):
            # replace only in non-code, non-link regions of the real line
            def wrap_real(m: re.Match) -> str:
                nonlocal wrapped
                pre = work[:m.start()]
                if pre.endswith("](") or pre.endswith("(") or pre.endswith('id="') \
                        or pre.endswith('"') or pre.endswith("`"):
                    return m.group(0)
                # inside an existing link text? if there's an unmatched [ before
                if pre.count("[") > pre.count("]"):
                    return m.group(0)
                secid = m.group(1)
                short = pretty_sec_text(secid)
                wrapped += 1
                return f"[{short}](#{secid})"

            work = re.sub(r"(?<![\w\"'(])(sec:[A-Za-z0-9._]+)", wrap_real, work)
        lines[i] = work
    if wrapped:
        notes.append(f"    wrapped {wrapped} bare sec: refs")
    if pretty:
        notes.append(f"    prettified {pretty} sec: link texts")
    return "\n".join(lines), wrapped, pretty, notes


# =============================================================== 7. images
def resolve_image(lang: str, name: str) -> str | None:
    manual = DOCS / lang / "images" / "manual"
    if "*" not in name:
        cand = manual / name
        return name if cand.exists() else None
    stem = name.split("*")[0]
    matches = sorted(
        p.name for p in manual.iterdir() if p.is_file() and p.name.startswith(stem)
    )
    exact = [m for m in matches if m.startswith(stem) and m[len(stem):].count(".") == 1]
    if exact:
        return exact[0]
    return matches[0] if matches else None


def fix_images(text: str, lang: str) -> tuple[str, int, list[str]]:
    notes: list[str] = []
    lines = text.split("\n")
    fence = fence_mask(lines)
    changed = 0
    for i, ln in enumerate(lines):
        if i in fence:
            continue

        def repl(m: re.Match) -> str:
            nonlocal changed
            alt, path = m.group("alt"), m.group("path")
            if path.startswith("http"):
                return m.group(0)
            fname = path.split("/")[-1]
            resolved = resolve_image(lang, fname)
            if resolved is None:
                notes.append(f"    ! unresolved image: {path}")
                return m.group(0)
            newpath = f"../../../images/manual/{resolved}"
            if path != newpath:
                changed += 1
            return f"![{alt}]({newpath})"

        lines[i] = IMG_RE.sub(repl, ln)
    if changed:
        notes.append(f"    fixed {changed} image paths")
    return "\n".join(lines), changed, notes


# ================================================================= driver
def process(lang: str, rel: str) -> list[str]:
    docs_path = DOCS / lang / CHAPTER / rel
    myst_path = MYSQ[lang] / CHAPTER_MYST / rel
    report = [f"{lang}/{rel}"]
    orig = docs_path.read_text(encoding="utf-8")
    text = orig

    myst_text = myst_path.read_text(encoding="utf-8") if myst_path.exists() else ""

    text, ntab, tnotes = fix_tables(text, myst_text)
    if ntab:
        report.append(f"  tables: {ntab} rebuilt")
        report.extend(tnotes)

    text, nfix, mnotes = fix_myst_fences(text)
    if nfix:
        report.append(f"  myst fences: {nfix} converted")
        report.extend(mnotes)

    text, nfield = fix_field_lines(text)
    if nfield:
        report.append(f"  orphan field lines: {nfield} removed")

    text, nspan = fix_span_roles(text)
    if nspan:
        report.append(f"  span roles: {nspan} stripped")

    text, mathnotes = fix_math(text)
    if mathnotes:
        report.append("  math:")
        report.extend(mathnotes)

    text, nanch, anotes = fix_eq_anchors(text)
    if nanch:
        report.append("  eq anchors:")
        report.extend(anotes)

    text, nwrap, npretty, snotes = fix_sec_refs(text)
    if nwrap or npretty:
        report.append("  sec refs:")
        report.extend(snotes)

    text, nimg, inotes = fix_images(text, lang)
    if nimg or inotes:
        report.append("  images:")
        report.extend(inotes)

    if text != orig:
        docs_path.write_text(text, encoding="utf-8")
    else:
        report.append("  (no change)")
    return report


def main() -> None:
    names = sorted(p.name for p in (DOCS / "en" / CHAPTER).glob("*.md"))
    for rel in names:
        for lang in ("en", "zh"):
            for line in process(lang, rel):
                print(line)
        print()


if __name__ == "__main__":
    main()
