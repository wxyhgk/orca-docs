#!/usr/bin/env python3
"""QA-fix ORCA manual spectroscopyproperties markdown for MkDocs (batch 4).

Fixes in docs/{en,zh}/manual/contents/spectroscopyproperties/:
  1. Half-converted flat-tables (`| Item | Value |` mini-tables + orphan
     bullets + nested `* -` rows) reassembled into one pipe table each,
     indented inside the `!!! note "caption"` admonition. Raw `* -`
     list-tables inside admonitions are converted the same way.
  2. Orphan Sphinx option lines (:header-rows: :class: :width: ...) -> removed.
  3. MyST roles {ref}/{numref}/{cite}/{eq}/{index} and `(name)=` targets fixed.
  4. Bare `sec:` link targets `(sec:label)` -> `(#sec:label)`;
     `[sec:label](#sec:label)` link text humanized to last two id segments.
  5. Image paths ../../images/NAME(.*) -> ../../../images/manual/NAME.ext.
  6. Math: multi-line inline `$...$` spans joined to one line (including
     frac-left/right splits); blank lines removed inside `$$`
     display blocks; stray \\tag{...} outside math dropped.
  7. Broken fences: ` ``` --> ` tails stripped (+ HTML comment unwrapped),
     unclosed EOF fence closed, true empty fences removed.
  8. Triple-backtick inline code ```` ```KEYWORD```` ```` -> `KEYWORD`.

Keeps code block bodies, ORCA keywords and <a id=...> labels. Does not translate.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs")
SPEC = "manual/contents/spectroscopyproperties"

FIELD_RE = re.compile(
    r"^[ \t]*:(?:width|class|header-rows|subcaptions|class-grid|align|scale"
    r"|name|alt|figwidth|figclass|option|stub-columns|widths|alignments"
    r"|tab-width|linenos|lines|dedent|encoding|start-after|end-before"
    r"|language|path|caption|figclass|numbered|reversed|maxdepth|glob"
    r"|hidden|titlesonly|header-rows|stub-columns):[^\n]*$"
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
MINI_HDR_RE = re.compile(r"^\| (Item \| Value|项目 \| 内容) \|$")
MINI_SEP_RE = re.compile(r"^\| [-| ]+\|$")
MINI_ROW_RE = re.compile(r"^\| \*\*(?P<name>.+?)\*\* \| (?:—|无) \|$")
BULLET_RE = re.compile(r"^(?P<ind>\s{4,})(?P<mark>[-*])(?: (?P<txt>.*))?$")
TRIPLE_INLINE_RE = re.compile(r"```([A-Za-z_{} .:/-]{1,60})```")

report: dict[str, list[str]] = {}


def note(path: Path, msg: str) -> None:
    report.setdefault(str(path), []).append(msg)


# ================================================================ shared utils
def fence_states(lines: list[str]) -> list[bool]:
    """True if the line is inside (or is) a fenced code block."""
    inside = [False] * len(lines)
    open_fence = False
    marker = ""
    for i, ln in enumerate(lines):
        m = FENCE_RE.match(ln)
        if m:
            if not open_fence:
                open_fence = True
                marker = m.group(2)
                inside[i] = True
            elif len(m.group(2)) >= len(marker) and not m.group(3).strip():
                inside[i] = True
                open_fence = False
                marker = ""
            else:
                inside[i] = True
            continue
        inside[i] = open_fence
    return inside


def table_to_pipe(grid: list[list[str]], ncols: int) -> list[str]:
    def esc(cell: str) -> str:
        return cell.replace("|", "\\|").strip()

    out = ["| " + " | ".join(esc(c) for c in grid[0]) + " |"]
    out.append("| " + " | ".join("---" for _ in range(ncols)) + " |")
    for r in grid[1:]:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return out


# ================================================================ fences
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
            note(str(path), f"L{i+1}: stripped trailing '-->' from fence closer")
    text2 = "\n".join(lines)

    # unwrap every `<!-- [>] ```lang` opener: superfences pairs fences before
    # HTML-comment handling, so a commented-out fence still participates in
    # fence pairing and an unclosed `<!--` comments out the rest of the page.
    # Intentional full-section `<!-- ... -->` comments (no fence on the
    # opener line) are left alone.
    for i, ln in enumerate(lines):
        if "<!--" not in ln:
            continue
        if not re.match(r"^[ \t]*<!--\s*>?\s*`{3,}", ln):
            continue
        new = re.sub(r"^([ \t]*)<!--\s*>\s*", r"\1", ln)
        if new == ln:
            new = re.sub(r"^([ \t]*)<!--\s*", r"\1", ln)
        if new != ln:
            lines[i] = new
            changed += 1
            note(str(path), f"L{i+1}: unwrapped commented fence opener")
    text2 = "\n".join(lines)

    # remove true empty fences (opener with language, no content)
    lines = text2.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if m and m.group(3).strip() and not m.group(3).strip().startswith("-->"):
            j = i + 1
            body: list[str] = []
            while j < len(lines):
                m2 = FENCE_RE.match(lines[j])
                if m2 and not m2.group(3).strip() and len(m2.group(2)) >= len(m.group(2)):
                    break
                body.append(lines[j])
                j += 1
            if j < len(lines) and not any(b.strip() for b in body):
                note(str(path), f"L{i+1}: removed empty fence {lines[i].strip()!r}")
                changed += 1
                i = j + 1
                continue
            out.append(lines[i])
            i += 1
            continue
        out.append(lines[i])
        i += 1
    text2 = "\n".join(out)

    # unterminated fence at EOF -> close
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
        note(str(path), f"L{oi+1}: unclosed fence closed at L{end+1}")
        text2 = "\n".join(lines)

    return text2 if changed else text


# ================================================================ MyST roles
def fix_roles(text: str, path: Path) -> str:
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

    def lbl(m: re.Match) -> str:
        note(str(path), f"({m.group(1)})= -> <a id>")
        return f'<a id="{m.group(1)}"></a>'

    text = LABEL_TARGET_RE.sub(lbl, text)
    text = SPAN_ROLE_RE.sub("", text)

    # mangled `](see Section {numref} \`sec:...`)` -> proper fragment link
    def mangled(m: re.Match) -> str:
        note(str(path), f"mangled numref link fixed: {m.group(1)}")
        return f"](#sec:{m.group(1).split('sec:')[-1]})"

    text = re.sub(
        r"\]\(see Section \{numref\} `sec:([^`]+)`\)",
        lambda m: f"](#sec:{m.group(1)})",
        text,
    )
    if text != before:
        note(str(path), "MyST roles/targets fixed")
    return text


# ================================================================ sec: links
def humanize_sec(label: str) -> str:
    """sec:aaa.bbb.ccc.ddd -> ccc.ddd (last two id segments)."""
    core = label.split("sec:", 1)[-1]
    parts = core.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else core


def fix_sec_links(text: str, path: Path) -> str:
    before = text
    n_bare = 0
    n_text = 0

    def repl(m: re.Match) -> str:
        nonlocal n_bare, n_text
        txt, tgt = m.group(1), m.group(2)
        if tgt.startswith("#sec:"):
            if txt.startswith("sec:"):
                n_text += 1
                return f"[{humanize_sec(txt)}](#{tgt[1:]})"
            return m.group(0)
        if tgt.startswith("sec:"):
            n_bare += 1
            return f"[{txt}](#{tgt})"
        return m.group(0)

    text = re.sub(r"\[([^\]]*)\]\(([^)]+)\)", repl, text)
    if n_bare:
        note(str(path), f"{n_bare} bare (sec:...) link target(s) -> (#sec:...)")
    if n_text:
        note(str(path), f"{n_text} sec: link text(s) humanized")
    return text if text != before else text


# ================================================================ images
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
    exact = [m for m in matches if m[len(stem):].count(".") == 1]
    return exact[0] if exact else (matches[0] if matches else None)


def fix_images(text: str, lang: str, path: Path) -> str:
    def repl(m: re.Match) -> str:
        alt, pth = m.group("alt"), m.group("path")
        if pth.startswith("http"):
            return m.group(0)
        fname = pth.split("/")[-1]
        resolved = resolve_image(lang, fname)
        if resolved is None:
            return m.group(0)
        new = f"![{alt}](../../../images/manual/{resolved})"
        if new != m.group(0):
            note(str(path), f"image path: {pth} -> ../../../images/manual/{resolved}")
        return new

    return IMG_RE.sub(repl, text)


# ================================================================ orphan options
def fix_orphan_options(text: str, path: Path) -> str:
    lines = text.split("\n")
    inf = fence_states(lines)
    out: list[str] = []
    for i, ln in enumerate(lines):
        if not inf[i] and FIELD_RE.match(ln):
            note(str(path), f"L{i+1}: dropped orphan option `{ln.strip()}`")
            continue
        out.append(ln)
    return "\n".join(out)


# ================================================================ triple-backtick inline
def fix_triple_inline(text: str, path: Path) -> str:
    def repl(m: re.Match) -> str:
        note(str(path), f"triple-backtick inline -> single: {m.group(0)!r}")
        return f"`{m.group(1)}`"

    return TRIPLE_INLINE_RE.sub(repl, text)


# ================================================================ math
CODE_SPAN_RE = re.compile(r"`+[^`]*`+")


def strip_code(line: str) -> str:
    return CODE_SPAN_RE.sub(lambda m: " " * len(m.group(0)), line)


def escape_orca_dollars(text: str, path: Path) -> str:
    """Escape `$` of ORCA `$name` variables written inside double quotes."""
    parts = re.split(r"(`+[^`]*`+)", text)
    changed = False
    for pi, part in enumerate(parts):
        if part.startswith("`"):
            continue

        def repl(m: re.Match) -> str:
            return m.group(0).replace("$", "\\$")

        np = re.sub(r'"\$[A-Za-z_][A-Za-z0-9_.]*"', repl, part)
        if np != part:
            parts[pi] = np
            changed = True
    if changed:
        note(str(path), "escaped ORCA $var in double quotes")
        return "".join(parts)
    return text


def single_dollars(line: str) -> list[int]:
    body = strip_code(line)
    out: list[int] = []
    i = 0
    while i < len(body):
        if body[i] == "\\":
            i += 2
            continue
        if body[i] == "$":
            if body[i:i + 2] == "$$":
                i += 2
                continue
            out.append(i)
            i += 1
            continue
        i += 1
    return out


def display_blocks(lines: list[str], in_fence: list[bool]) -> list[tuple[int, int]]:
    blocks: list[tuple[int, int]] = []
    i = 0
    n = len(lines)
    while i < n:
        if in_fence[i]:
            i += 1
            continue
        if "$$" not in lines[i]:
            i += 1
            continue
        if lines[i].count("$$") % 2 == 1:
            start = i
            j = i + 1
            while j < n:
                if in_fence[j]:
                    j += 1
                    continue
                if lines[j].count("$$") % 2 == 1:
                    blocks.append((start, j))
                    i = j + 1
                    break
                j += 1
            else:
                blocks.append((start, n - 1))
                i = n
            continue
        blocks.append((i, i))
        i += 1
    return blocks


def fix_math(text: str, path: Path) -> str:
    text = escape_orca_dollars(text, path)
    lines = text.split("\n")
    inf = fence_states(lines)
    blocks = display_blocks(lines, inf)
    in_disp = [False] * len(lines)
    for a, b in blocks:
        for k in range(a, b + 1):
            in_disp[k] = True

    # 1) strip blank lines inside $$ display blocks (arithmatex: blank lines
    #    inside the block silently disable math). Reverse order so earlier
    #    edits don't shift later block indices.
    for a, b in sorted(blocks, reverse=True):
        if a >= b:
            continue
        inner = lines[a + 1:b]
        if any(not x.strip() for x in inner):
            lines[a + 1:b] = [x for x in inner if x.strip()]
            note(str(path), f"L{a+1}: removed blank line(s) inside $$ display block")
    # 1b) normalize $$ delimiter lines to exactly '$$' (trailing whitespace
    #     breaks arithmatex recognition)
    for i, ln in enumerate(lines):
        if inf[i]:
            continue
        s = ln.strip()
        if s == "$$" and ln != "$$":
            lines[i] = "$$"
            note(str(path), f"L{i+1}: normalized $$ delimiter whitespace")

    # recompute after mutation
    inf = fence_states(lines)
    blocks = display_blocks(lines, inf)
    in_disp = [False] * len(lines)
    for a, b in blocks:
        for k in range(a, b + 1):
            in_disp[k] = True

    # 2) ensure blank line before/after display blocks
    insert_before: set[int] = set()
    insert_after: set[int] = set()
    for a, b in blocks:
        if a > 0 and lines[a - 1].strip() and not inf[a - 1] and not in_disp[a - 1]:
            insert_before.add(a)
        if b + 1 < len(lines) and lines[b + 1].strip() and not inf[b + 1] and not in_disp[b + 1]:
            insert_after.add(b)
    if insert_before or insert_after:
        rebuilt: list[str] = []
        for i, ln in enumerate(lines):
            if i in insert_before and (not rebuilt or rebuilt[-1].strip() != ""):
                rebuilt.append("")
            rebuilt.append(ln)
            if i in insert_after:
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                if nxt.strip() != "":
                    rebuilt.append("")
        lines = rebuilt
        note(str(path), "added blank line(s) around $$ display block(s)")
        inf = fence_states(lines)
        blocks = display_blocks(lines, inf)
        in_disp = [False] * len(lines)
        for a, b in blocks:
            for k in range(a, b + 1):
                in_disp[k] = True

    # 3) join multi-line inline $...$ spans (incl. \frac{\left(...\right)} splits)
    n = len(lines)
    result: list[str] = []
    i = 0
    while i < n:
        ln = lines[i]
        if inf[i] or in_disp[i]:
            result.append(ln)
            i += 1
            continue
        if len(single_dollars(ln)) % 2 == 0:
            result.append(ln)
            i += 1
            continue
        run = [ln]
        j = i + 1
        closed = False
        while j < n:
            if inf[j] or in_disp[j]:
                break
            if lines[j].strip() == "":
                break
            if re.match(r"^\s*([-*+] |\d+\. |#{1,6} |!!!|\| )", lines[j]):
                break
            run.append(lines[j])
            if len(single_dollars(lines[j])) % 2 == 1:
                closed = True
                break
            j += 1
        if closed:
            merged = run[0].rstrip()
            for cont in run[1:]:
                merged += " " + cont.strip()
            result.append(merged)
            note(str(path), f"L{i+1}: joined multi-line inline $...$ span")
            i = j + 1
        else:
            result.append(ln)
            i += 1

    # 4) stray \tag{...} outside math
    for k, ln in enumerate(result):
        if inf[k] or (k < len(in_disp) and in_disp[k]):
            continue
        no_math = re.sub(r"(?<!\\)\$[^$]*(?<!\\)\$", " ", strip_code(ln))
        if re.search(r"\\tag\s*\{", no_math):
            new = re.sub(r"\\tag\s*\{[^}]*\}", "", ln)
            if new != ln:
                result[k] = new
                note(str(path), f"L{k+1}: removed stray \\tag outside math")

    return "\n".join(result)


# ================================================================ tables
def parse_bullets(lines: list[str], start: int, stop: int) -> tuple[list[str], int]:
    """Collect orphan bullet cells (indent>=4) between start and stop."""
    cells: list[str] = []
    i = start
    cur: list[str] = []
    cur_ind: int | None = None

    def flush() -> None:
        nonlocal cur
        if cur_ind is not None:
            cells.append(" ".join(x for x in cur if x).strip())
        cur = []

    while i < stop:
        ln = lines[i]
        if ln.strip() == "":
            flush()
            cur_ind = None
            i += 1
            continue
        m = BULLET_RE.match(ln)
        if m and m.group("mark") == "-":
            flush()
            cur_ind = len(m.group("ind"))
            cur = [m.group("txt") or ""]
            i += 1
            continue
        if cur_ind is not None and len(ln) - len(ln.lstrip()) > cur_ind:
            cur.append(ln.strip())
            i += 1
            continue
        break
    flush()
    return cells, i


def parse_nested_rows(lines: list[str], start: int, stop: int) -> tuple[list[list[str]], int]:
    """Collect nested `* -` list-table rows (indent 2-6) with `- ` cells."""
    rows: list[list[str]] = []
    i = start
    while i < stop:
        m = CELL_START_RE.match(lines[i])
        if not m:
            break
        row: list[str] = []
        cell_indent = len(m.group(1)) + 2
        cur = [m.group(2) or ""]
        i += 1
        while i < stop:
            ln = lines[i]
            if ln.strip() == "":
                k = i + 1
                while k < stop and lines[k].strip() == "":
                    k += 1
                if k < stop and CELL_CONT_RE.match(lines[k]) and \
                        len(CELL_CONT_RE.match(lines[k]).group(1)) == cell_indent:
                    row.append(" ".join(cur).strip())
                    cur = []
                    i = k
                    continue
                break
            mc = CELL_CONT_RE.match(ln)
            if mc and len(mc.group(1)) == cell_indent:
                row.append(" ".join(cur).strip())
                cur = [mc.group(2) or ""]
                i += 1
                continue
            if len(ln) - len(ln.lstrip()) > cell_indent:
                cur.append(ln.strip())
                i += 1
                continue
            break
        row.append(" ".join(cur).strip())
        rows.append(row)
    return rows, i


def find_run_end(lines: list[str], i: int) -> int:
    """End index (exclusive) of a flat-table run starting at mini-header i."""
    n = len(lines)
    j = i
    while j < n:
        ln = lines[j]
        if MINI_HDR_RE.match(ln):
            j += 1
            continue
        if MINI_SEP_RE.match(ln) or MINI_ROW_RE.match(ln):
            j += 1
            continue
        if BULLET_RE.match(ln):
            j += 1
            continue
        if CELL_START_RE.match(ln) or CELL_CONT_RE.match(ln):
            j += 1
            continue
        if ln.strip() == "":
            # blank allowed inside run only if run continues after
            k = j + 1
            while k < n and lines[k].strip() == "":
                k += 1
            if k < n and (
                MINI_HDR_RE.match(lines[k]) or MINI_ROW_RE.match(lines[k])
                or BULLET_RE.match(lines[k]) or CELL_START_RE.match(lines[k])
            ):
                j = k
                continue
            return j
        return j
    return n


def convert_mini_run(run: list[str], path: Path) -> list[str]:
    """Convert a run of mini-tables / nested rows into one pipe table."""
    rows: list[list[str]] = []
    i = 0
    n = len(run)
    while i < n:
        if MINI_HDR_RE.match(run[i]):
            # skip header + separator
            i += 1
            if i < n and MINI_SEP_RE.match(run[i]):
                i += 1
            continue
        m = MINI_ROW_RE.match(run[i])
        if m:
            name = m.group("name")
            i += 1
            # optional blank then bullets
            k = i
            while k < n and run[k].strip() == "":
                k += 1
            cells, k2 = parse_bullets(run, k, n)
            row = [name] + cells
            # nested `* -` continuation rows follow: if this row is narrower,
            # the dropped empty cell(s) belong in the middle (Options column)
            nk = k2
            while nk < n and run[nk].strip() == "":
                nk += 1
            if nk < n and CELL_START_RE.match(run[nk]):
                nrows, _ = parse_nested_rows(run, nk, n)
                if nrows and len(row) < max(len(r) for r in nrows):
                    deficit = max(len(r) for r in nrows) - len(row)
                    row = [row[0]] + [""] * deficit + row[1:]
            rows.append(row)
            i = k2
            continue
        if CELL_START_RE.match(run[i]):
            nrows, i = parse_nested_rows(run, i, n)
            rows.extend(nrows)
            continue
        if run[i].strip() == "":
            i += 1
            continue
        # unknown line: keep as-is by aborting to a bullet-free row
        i += 1
    if not rows:
        return []
    ncols = max(len(r) for r in rows)
    grid = [r + [""] * (ncols - len(r)) for r in rows]
    note(str(path), f"flat-table -> {ncols}-column pipe table ({len(rows)} rows)")
    return table_to_pipe(grid, ncols)


def is_list_table(body: list[str]) -> bool:
    content = [ln for ln in body if ln.strip() and not FIELD_RE.match(ln)]
    if not content:
        return False
    cell_indent: int | None = None
    saw_row = False
    for ln in content:
        if CELL_START_RE.match(ln):
            cell_indent = len(CELL_START_RE.match(ln).group(1)) + 2
            saw_row = True
            continue
        m = CELL_CONT_RE.match(ln)
        if m and cell_indent is not None and len(m.group(1)) == cell_indent:
            continue
        indent = len(ln) - len(ln.lstrip())
        if cell_indent is not None and indent > cell_indent:
            continue
        return False
    return saw_row


def convert_list_table_body(body: list[str], path: Path) -> list[str]:
    content = [ln for ln in body if ln.strip() and not FIELD_RE.match(ln)]
    rows, _ = parse_nested_rows(content, 0, len(content))
    if not rows:
        return []
    ncols = max(len(r) for r in rows)
    grid = [r + [""] * (ncols - len(r)) for r in rows]
    if ncols <= 1:
        bullets = [f"* {r[0].strip()}" for r in rows if r and r[0].strip()]
        note(str(path), f"list-table -> {len(bullets)} bullet(s)")
        return bullets
    note(str(path), f"list-table -> {ncols}-column pipe table ({len(rows)} rows)")
    return table_to_pipe(grid, ncols)


def fix_tables(text: str, path: Path) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        # --- raw list-table inside an admonition (re-detect admonition body)
        m_adm = ADMON_RE.match(lines[i])
        if m_adm:
            out.append(lines[i])
            i += 1
            # collect admonition body (indented)
            body_start = i
            body: list[str] = []
            j = i
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
            kept: list[str] = []
            for ln in body:
                if FIELD_RE.match(ln):
                    note(str(path), f"L{body_start+1}: dropped orphan option `{ln.strip()}`")
                    continue
                kept.append(ln)
            while kept and kept[0].strip() == "":
                kept.pop(0)
            while kept and kept[-1].strip() == "":
                kept.pop()
            if is_list_table(kept):
                kept = convert_list_table_body(kept, path)
            for ln in kept:
                out.append(("    " + ln) if ln.strip() else "")
            # keep a blank line between the admonition and following prose
            if j < n and lines[j].strip() != "" and (not out or out[-1].strip() != ""):
                out.append("")
            i = j
            continue

        # --- half-converted mini-table run
        if MINI_HDR_RE.match(lines[i]):
            j = find_run_end(lines, i)
            pipe = convert_mini_run(lines[i:j], path)
            # indent table if it directly follows a `!!! note` option block
            indent = ""
            back = len(out) - 1
            saw_admon = False
            while back >= 0 and (out[back].strip() == "" or FIELD_RE.match(out[back])):
                if FIELD_RE.match(out[back]):
                    # drop orphan option lines above the run
                    note(str(path), f"dropped orphan option `{out[back].strip()}` above table")
                    out.pop(back)
                back -= 1
            if back >= 0 and ADMON_RE.match(out[back]):
                saw_admon = True
            if saw_admon:
                indent = "    "
                # ensure blank line between admonition header and table body
                if out and out[-1].strip() != "":
                    pass
            for ln in pipe:
                out.append(indent + ln)
            # keep a blank line between the table and following prose
            if i < n and lines[i].strip() != "" and (not out or out[-1].strip() != ""):
                out.append("")
            # skip trailing blanks consumed by run
            i = j
            while i < n and lines[i].strip() == "" and i + 1 < n and not lines[i + 1].strip():
                i += 1
            continue

        out.append(lines[i])
        i += 1

    return "\n".join(out)


# ================================================================ glue
def process_file(path: Path, lang: str) -> None:
    orig = path.read_text(encoding="utf-8")
    text = orig
    text = fix_broken_fences(text, path)
    text = fix_roles(text, path)
    text = fix_sec_links(text, path)
    text = fix_tables(text, path)
    text = fix_orphan_options(text, path)
    text = fix_images(text, lang, path)
    text = fix_triple_inline(text, path)
    text = fix_math(text, path)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        note(str(path), "updated")
    else:
        note(str(path), "no change")


def main() -> None:
    for lang in ("en", "zh"):
        d = ROOT / lang / SPEC
        for f in sorted(d.glob("*.md")):
            process_file(f, lang)
    for path, msgs in sorted(report.items()):
        if msgs != ["no change"]:
            print(f"{path}:")
            for msg in msgs:
                print(f"  - {msg}")
        else:
            print(f"{path}: no change")


if __name__ == "__main__":
    main()
