#!/usr/bin/env python3
"""Fix spectroscopyproperties Manual markdown.

1. MyST list-table remnants (`* -` rows) inside `!!! note` -> Markdown pipe tables
   (house style: `| a | b |` + `| --- | --- |`), keeping ORCA keywords.
2. Math defects: join multi-line inline `$...$` spans, restore `\\right`
   fragments corrupted by \\r-escape, escape literal ORCA `$` variables,
   drop empty `$ $` spans, ensure `$$` display blocks balanced with blank
   lines around them, remove stray `\\tag{...}` outside math.

Does not translate. Cell/text content is preserved except math whitespace.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs")
SPEC = "manual/contents/spectroscopyproperties"

TABLE_FILES = {
    "en": ["eom.md", "epr.md", "hfld.md", "moessbauer.md", "nocv.md",
           "population.md", "spinorbit.md", "esd.md", "led.md"],
    "zh": ["eom.md", "epr.md", "hfld.md", "moessbauer.md", "nocv.md",
           "population.md", "spinorbit.md"],
}

# ------------------------------------------------------------ shared regexes
FIELD_RE = re.compile(
    r"^[ \t]*:(?:width|class|header-rows|subcaptions|class-grid|align|scale"
    r"|name|alt|figwidth|figclass|option|stub-columns|widths|alignments"
    r"|header-rows|stub-columns):[^\n]*$"
)
CELL_START_RE = re.compile(r"^(\s*)\* -(?: (.*))?$")
CELL_CONT_RE = re.compile(r"^(\s*)-(?: (.*))?$")
ADMON_RE = re.compile(
    r'^(!!!\s+(?P<kind>note|tip|warning|info|abstract|success|question|failure|bug|example|quote))'
    r'(?P<title>\s+"(?P<t>[^"]*)")?[ \t]*$'
)
FENCE_RE = re.compile(r"^([ \t]*)(`{3,})(.*)$")

report: list[str] = []


def note(msg: str) -> None:
    report.append(msg)


# ================================================================ list-tables
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


def table_to_pipe(grid: list[list[str]], ncols: int) -> list[str]:
    def esc(cell: str) -> str:
        return cell.replace("|", "\\|").strip()

    out = ["| " + " | ".join(esc(c) for c in grid[0]) + " |"]
    out.append("| " + " | ".join("---" for _ in range(ncols)) + " |")
    for r in grid[1:]:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return out


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


def convert_list_table_body(body: list[str]) -> list[str]:
    rows = parse_list_table([ln for ln in body if ln.strip() and not FIELD_RE.match(ln)])
    ncols = max((len(r) for r in rows), default=0)
    grid = [r + [""] * (ncols - len(r)) for r in rows]
    if ncols <= 1:
        bullets = [f"* {r[0].strip()}" for r in rows if r and r[0].strip()]
        note(f"list-table -> {len(bullets)} bullet(s)")
        return bullets
    pipe = table_to_pipe(grid, ncols)
    note(f"list-table -> {ncols}-column pipe table ({len(rows)} rows)")
    return pipe


def process_admonitions(text: str) -> str:
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

        kept: list[str] = []
        dropped_option = False
        for ln in body:
            if FIELD_RE.match(ln):
                dropped_option = True
                note(f"L{i+1}: dropped orphan option `{ln.strip()}`")
                continue
            kept.append(ln)
        while kept and kept[0].strip() == "":
            kept.pop(0)
        while kept and kept[-1].strip() == "":
            kept.pop()

        if is_list_table(kept):
            kept = convert_list_table_body(kept)

        out.append(f'{header} "{title}"' if title else header)
        for ln in kept:
            out.append(("    " + ln) if ln.strip() else "")
        i = j

    return "\n".join(out)


# ================================================================ math
CODE_SPAN_RE = re.compile(r"`+[^`]*`+")


def strip_code(line: str) -> str:
    return CODE_SPAN_RE.sub(lambda m: " " * len(m.group(0)), line)


def single_dollars(line: str) -> list[int]:
    """Positions of `$` that are not `$$`, not escaped, outside code spans."""
    body = strip_code(line)
    out = []
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "$":
            if body[i:i + 2] == "$$":
                i += 2
                continue
            out.append(i)
            i += 1
            continue
        i += 1
    return out


def fix_ight(line: str) -> str:
    """Restore `\\right` corrupted to `ight` by \\r escape eating."""
    return re.sub(r"(?<![A-Za-z\\])ight(\\\})", r"\\right\1", line)


def escape_literal_orca_dollar(line: str) -> str:
    """Escape `$` of ORCA `$name` variables written inside double quotes."""
    parts = re.split(r"(`+[^`]*`+)", line)
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
    return "".join(parts) if changed else line


def line_in_fence_states(lines: list[str]) -> list[bool]:
    """True if line is inside a fenced code block (not counting fence lines)."""
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


def display_blocks(lines: list[str], in_fence: list[bool]) -> list[tuple[int, int]]:
    """Return (start, end) inclusive line ranges of $$ display blocks."""
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        if in_fence[i]:
            i += 1
            continue
        line = lines[i]
        if "$$" not in line:
            i += 1
            continue
        # count $$ toggles
        cnt = line.count("$$")
        if cnt % 2 == 1:
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
        else:
            blocks.append((i, i))
            i += 1
    return blocks


def fix_math_text(text: str) -> tuple[str, dict[str, int]]:
    stats = {
        "ight_restored": 0,
        "orca_dollar_escaped": 0,
        "inline_spans_joined": 0,
        "empty_inline_removed": 0,
        "tag_outside_removed": 0,
        "display_blank_added": 0,
    }
    # 0) restore corrupted \right
    lines = text.split("\n")
    fence_state = line_in_fence_states(lines)
    for i, ln in enumerate(lines):
        if fence_state[i]:
            continue
        new = fix_ight(ln)
        if new != ln:
            stats["ight_restored"] += 1
            lines[i] = new

    # 1) escape literal ORCA $ variables in quotes
    for i, ln in enumerate(lines):
        if fence_state[i]:
            continue
        new = escape_literal_orca_dollar(ln)
        if new != ln:
            stats["orca_dollar_escaped"] += new.count("\\$") - ln.count("\\$")
            lines[i] = new

    in_fence = line_in_fence_states(lines)
    blocks = display_blocks(lines, in_fence)
    in_disp = [False] * len(lines)
    for a, b in blocks:
        for k in range(a, b + 1):
            in_disp[k] = True

    # 2) ensure blank line before/after display blocks (and balance is structural)
    out_lines = lines[:]
    insert_before: set[int] = set()
    insert_after: set[int] = set()
    for a, b in blocks:
        if a > 0 and out_lines[a - 1].strip() \
                and not in_fence[a - 1] and not in_disp[a - 1]:
            insert_before.add(a)
        if b + 1 < len(out_lines) and out_lines[b + 1].strip() \
                and not in_fence[b + 1] and not in_disp[b + 1]:
            insert_after.add(b)
    if insert_before or insert_after:
        rebuilt: list[str] = []
        for i, ln in enumerate(out_lines):
            if i in insert_before and (not rebuilt or rebuilt[-1].strip() != ""):
                rebuilt.append("")
                stats["display_blank_added"] += 1
            rebuilt.append(ln)
            if i in insert_after:
                # look at next line
                nxt = out_lines[i + 1] if i + 1 < len(out_lines) else ""
                if nxt.strip() != "":
                    rebuilt.append("")
                    stats["display_blank_added"] += 1
        out_lines = rebuilt
        in_fence = line_in_fence_states(out_lines)
        blocks = display_blocks(out_lines, in_fence)
        in_disp = [False] * len(out_lines)
        for a, b in blocks:
            for k in range(a, b + 1):
                in_disp[k] = True

    # 3) remove stray \tag{...} outside math
    for i, ln in enumerate(out_lines):
        if in_fence[i] or in_disp[i]:
            continue
        body = strip_code(ln)
        # remove inline math spans, then look for \tag
        no_math = re.sub(r"(?<!\\)\$[^$]*(?<!\\)\$", " ", body)
        if re.search(r"\\tag\s*\{", no_math):
            # remove \tag{...} from the real line (outside code)
            new = re.sub(r"\\tag\s*\{[^}]*\}", "", ln)
            if new != ln:
                stats["tag_outside_removed"] += 1
                out_lines[i] = new

    # 4) remove empty inline `$ $` (pair-based; `$x$ $y$` boundaries are kept)
    for i, ln in enumerate(out_lines):
        if in_fence[i] or in_disp[i]:
            continue
        parts = re.split(r"(`+[^`]*`+)", ln)
        changed = False
        for pi, part in enumerate(parts):
            if part.startswith("`"):
                continue
            pos: list[int] = []
            k = 0
            while k < len(part):
                if part[k] == "\\":
                    k += 2
                    continue
                if part[k] == "$" and part[k:k + 2] != "$$":
                    pos.append(k)
                    k += 1
                    continue
                k += 1
            drop: set[int] = set()
            for a in range(0, len(pos) - 1, 2):
                apos, bpos = pos[a], pos[a + 1]
                if part[apos + 1:bpos].strip() == "":
                    drop.add(apos)
                    drop.add(bpos)
            if drop:
                parts[pi] = "".join(ch for k, ch in enumerate(part) if k not in drop)
                changed = True
                stats["empty_inline_removed"] += len(drop) // 2
        if changed:
            out_lines[i] = "".join(parts)

    # 5) join multi-line inline $...$ spans
    in_fence = line_in_fence_states(out_lines)
    blocks = display_blocks(out_lines, in_fence)
    in_disp = [False] * len(out_lines)
    for a, b in blocks:
        for k in range(a, b + 1):
            in_disp[k] = True

    n = len(out_lines)
    result: list[str] = []
    i = 0
    while i < n:
        ln = out_lines[i]
        if in_fence[i] or in_disp[i]:
            result.append(ln)
            i += 1
            continue
        dollars = single_dollars(ln)
        if len(dollars) % 2 == 0:
            result.append(ln)
            i += 1
            continue
        # odd -> unclosed; gather run
        run = [ln]
        j = i + 1
        closed = False
        while j < n:
            if in_fence[j] or in_disp[j]:
                break
            if out_lines[j].strip() == "":
                break
            # stop at a new list item / heading to avoid swallowing structure
            if re.match(r"^\s*([-*+] |\d+\. |#{1,6} |!!!)", out_lines[j]):
                break
            d2 = single_dollars(out_lines[j])
            run.append(out_lines[j])
            if len(d2) % 2 == 1:
                closed = True
                break
            j += 1
        if closed:
            merged = run[0].rstrip()
            for cont in run[1:]:
                merged += " " + cont.strip()
            result.append(merged)
            stats["inline_spans_joined"] += 1
            i = j + 1
        else:
            # cannot close without crossing a boundary; leave as-is
            result.append(ln)
            i += 1

    return "\n".join(result), stats


# ================================================================ glue
def process_file(path: Path, do_tables: bool) -> None:
    orig = path.read_text(encoding="utf-8")
    text = orig
    tbl_stats = []
    if do_tables:
        before = len(report)
        text = process_admonitions(text)
        tbl_stats = report[before:]
    text, mstats = fix_math_text(text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        note(f"{path.relative_to(ROOT)}: UPDATED")
    else:
        note(f"{path.relative_to(ROOT)}: no change")
    for s in tbl_stats:
        note(f"  table: {s}")
    for k, v in mstats.items():
        if v:
            note(f"  math: {k}={v}")


def main() -> None:
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for lang in ("en", "zh"):
        d = ROOT / lang / SPEC
        for f in sorted(d.glob("*.md")):
            do_tables = which in ("all", "tables") and f.name in TABLE_FILES.get(lang, [])
            do_math = which in ("all", "math")
            if not (do_tables or do_math):
                continue
            process_file(f, do_tables)
    print("\n".join(report))


if __name__ == "__main__":
    main()
