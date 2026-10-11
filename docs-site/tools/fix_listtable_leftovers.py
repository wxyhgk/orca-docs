#!/usr/bin/env python3
"""Convert leftover MyST flat/list-table cells (`* -`) to proper Markdown pipe tables.

Parses the ORIGINAL MyST source (md/manual/{en,zh}) which still has
{cspan}/{rspan} span roles, builds a cell grid, emits pipe tables, and
replaces the corresponding `!!! note` blocks in docs-site markdown.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca")
MYSQ = {"en": ROOT / "md/manual/en", "zh": ROOT / "md/manual/zh"}
DOCS = {"en": ROOT / "docs-site/docs/en/manual", "zh": ROOT / "docs-site/docs/zh/manual"}

FILES = [
    "contents/moleculardynamics/moldyn.md",
    "contents/workflowsautomatization/compounddetails.md",
    "contents/utilitiesvisualization/utilities.md",
    "contents/orcaarchitecture/components.md",
    "contents/orcaarchitecture/conversionfactors.md",
    "contents/multiscalesimulations/qmmm-general.md",
    "contents/multiscalesimulations/qmmm-crystal.md",
]

SPAN_RE = re.compile(r"\{([cr])span\}`(\d+)`")
DIRECTIVE_RE = re.compile(
    r"^:::\{(?P<kind>flat-table|list-table)\}[ \t]*(?P<title>[^\n]*)\n"
    r"(?P<body>.*?)^:::[ \t]*$",
    re.M | re.S,
)

SECTION_LABELS = {
    "en": ("Mandatory Arguments", "Optional Arguments", "Modifiers", "Manadory Arguments"),
    "zh": ("必选参数", "可选参数", "修饰符"),
}


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
    return content, cspan, rspan


def parse_rows(body: str) -> list[list[tuple[str, int, int]]]:
    rows: list[list[tuple[str, int, int]]] = []
    for line in body.splitlines():
        if not line.strip():
            continue
        m_row = re.match(r"^\s*\* -[ \t]*(.*)$", line)
        if m_row:
            content, cs, rs = strip_spans(m_row.group(1))
            rows.append([(content, cs + 1, rs + 1)])
            continue
        m_cell = re.match(r"^[ \t]+-[ \t]*(.*)$", line)
        if m_cell and rows:
            content, cs, rs = strip_spans(m_cell.group(1))
            rows[-1].append((content, cs + 1, rs + 1))
    return rows


def build_grid(rows: list[list[tuple[str, int, int]]]) -> list[list[str]]:
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
                        grid[rj][cj] = text if (dr == 0 and dc == 0) else ""
            ci += cs
    return [[c if c is not None else "" for c in row] for row in grid]


def esc_pipe(text: str) -> str:
    return text.replace("|", "\\|")


def grid_to_pipe(grid: list[list[str]], header_rows: int) -> str:
    if not grid:
        return ""
    ncols = len(grid[0])
    lines: list[str] = []
    if header_rows > 0:
        for r in range(header_rows):
            lines.append("| " + " | ".join(esc_pipe(c) for c in grid[r]) + " |")
        lines.append("|" + "---|" * ncols)
        data_start = header_rows
    else:
        lines.append("| " + " | ".join([""] * ncols) + " |")
        lines.append("|" + "---|" * ncols)
        data_start = 0
    for r in range(data_start, len(grid)):
        lines.append("| " + " | ".join(esc_pipe(c) for c in grid[r]) + " |")
    return "\n".join(lines)


def is_section_label(text: str, lang: str) -> str | None:
    t = text.strip().rstrip(":：").strip()
    for lab in SECTION_LABELS.get(lang, SECTION_LABELS["en"]):
        if t == lab:
            return lab
    return None


def is_param_box(rows: list[list[tuple[str, int, int]]], lang: str) -> bool:
    return any(r and is_section_label(r[0][0], lang) for r in rows)


def render_param_box(grid: list[list[str]], lang: str) -> str:
    """Render a command parameter box as section headings + pipe tables.

    Grid columns (after span expansion):
      0: section label (or empty on continuation rows)
      1: modifier name (modifiers section) / empty (args section, label spans 2)
      2: parameter name
      3: type
      4: values
    """
    # Split into sections
    sections: list[tuple[str, list[list[str]]]] = []
    current_label = ""
    current_rows: list[list[str]] = []
    for row in grid:
        key = is_section_label(row[0], lang)
        if key:
            if current_label or current_rows:
                sections.append((current_label, current_rows))
            current_label = key
            current_rows = []
            # remainder of this row (after the label cell) is first data row
            rest = row[1:] if len(row) > 1 else []
            # For args sections the label spans cols 0-1 so data starts at col2.
            # For modifiers the label is col0 only and data starts at col1.
            # Detect: if row[1] is empty and row[2] non-empty → args layout.
            if row[1] == "" and any(row[2:]):
                data = ["", "", row[2], row[3] if len(row) > 3 else "",
                        row[4] if len(row) > 4 else ""]
                # Will be normalized below to 4-col (name, type, values)
                current_rows.append([row[2], row[3] if len(row) > 3 else "",
                                     row[4] if len(row) > 4 else ""])
            elif row[1] == "" and not any(row[2:]):
                # empty section e.g. "Mandatory Arguments:" with only "—"
                # find the dash somewhere in the row
                dash = ""
                for c in row:
                    if c.strip() in ("—", "-", "–"):
                        dash = "—"
                        break
                current_rows.append([dash or "—", "", ""])
            else:
                # modifiers layout: row[1]=name, row[2]=param, row[3]=type, row[4]=values
                current_rows.append([row[1], row[2], row[3] if len(row) > 3 else "",
                                     row[4] if len(row) > 4 else ""])
        else:
            # continuation row
            if current_label in ("Modifiers", "修饰符"):
                # modifier row: name may be empty (continuation of multi-param modifier)
                current_rows.append([row[1], row[2], row[3] if len(row) > 3 else "",
                                     row[4] if len(row) > 4 else ""])
            else:
                # args continuation: content at col2,3,4
                current_rows.append([row[2], row[3] if len(row) > 3 else "",
                                     row[4] if len(row) > 4 else ""])
    if current_label or current_rows:
        sections.append((current_label, current_rows))

    parts: list[str] = []
    for label, srows in sections:
        if not label:
            continue
        # Determine column count for this section
        has_param_col = label in ("Modifiers", "修饰符")
        if has_param_col:
            headers = ["Modifier", "Parameter", "Type", "Values"]
        else:
            headers = ["Parameter", "Type", "Values"]

        # Normalize rows to the right column count
        norm: list[list[str]] = []
        for r in srows:
            if has_param_col:
                r4 = (r + [""] * 4)[:4]
                # If row is ["—", "", "", ""] (empty section), keep as is
                norm.append(r4)
            else:
                # args: rows are [name, type, values] already
                r3 = (r + [""] * 3)[:3]
                norm.append(r3)

        # If section is "empty" (single row that's just a dash), render as one-liner
        if len(norm) == 1 and norm[0][0].strip() in ("—", "-", "–", "") and not any(
            c.strip() for c in norm[0][1:]
        ):
            parts.append(f"**{label}:** —")
            continue

        ncols = len(headers)
        table_lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * ncols]
        for r in norm:
            table_lines.append("| " + " | ".join(esc_pipe(c) for c in r) + " |")
        parts.append(f"**{label}:**\n\n" + "\n".join(table_lines))

    return "\n\n".join(parts)


def extract_myst_tables(text: str, lang: str) -> list[dict]:
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
        grid = build_grid(rows)
        tables.append({
            "title": title,
            "header_rows": header_rows,
            "grid": grid,
            "rows": rows,
            "is_param_box": is_param_box(rows, lang),
        })
    return tables


NOTE_START_RE = re.compile(r"^(?P<indent>[ \t]*)!!! note(?P<title>[^\n]*)$")


def find_star_dash_notes(text: str) -> list[tuple[int, int, str]]:
    lines = text.split("\n")
    blocks = []
    i = 0
    while i < len(lines):
        m = NOTE_START_RE.match(lines[i])
        if not m:
            i += 1
            continue
        indent = m.group("indent")
        title = m.group("title").strip()
        j = i + 1
        body_lines = []
        while j < len(lines):
            ln = lines[j]
            if ln.strip() == "":
                k = j + 1
                while k < len(lines) and lines[k].strip() == "":
                    k += 1
                if k < len(lines) and lines[k].startswith(indent + "    "):
                    body_lines.append(ln)
                    j += 1
                    continue
                break
            if ln.startswith(indent + "    ") or (indent == "" and ln.startswith("    ")):
                body_lines.append(ln)
                j += 1
                continue
            break
        body = "\n".join(body_lines)
        if "* -" in body:
            blocks.append((i, j, title))
        i = j
    return blocks


def convert_file(rel: str, lang: str) -> dict:
    myst_path = MYSQ[lang] / rel
    docs_path = DOCS[lang] / rel
    report = {"file": f"{lang}/{rel}", "before": 0, "after": 0, "tables": 0}

    myst_text = myst_path.read_text(encoding="utf-8")
    docs_text = docs_path.read_text(encoding="utf-8")

    tables = extract_myst_tables(myst_text, lang)
    note_blocks = find_star_dash_notes(docs_text)

    report["before"] = len(re.findall(r"^\s*\* -", docs_text, re.M))

    if len(tables) != len(note_blocks):
        report["error"] = f"mismatch: {len(tables)} myst vs {len(note_blocks)} notes"
        return report

    lines = docs_text.split("\n")
    for t, (start, end, note_title) in reversed(list(zip(tables, note_blocks))):
        grid = t["grid"]
        title = (t["title"] or note_title.strip('"').strip()).strip()

        if t["is_param_box"]:
            content = render_param_box(grid, lang)
        else:
            hr = t["header_rows"]
            if hr == 0 and title:
                hr = 1  # titled tables always have a header row
            content = grid_to_pipe(grid, hr)

        if title:
            indented = "\n".join(
                ("    " + ln) if ln.strip() else "" for ln in content.splitlines()
            )
            repl = f'!!! note "{title}"\n{indented}\n'
        else:
            repl = content + "\n"

        lines[start:end] = repl.split("\n")
        report["tables"] += 1

    new_text = "\n".join(lines)
    report["after"] = len(re.findall(r"^\s*\* -", new_text, re.M))
    if new_text != docs_path.read_text(encoding="utf-8"):
        docs_path.write_text(new_text, encoding="utf-8")
        report["written"] = True
    return report


def main() -> None:
    for rel in FILES:
        for lang in ("en", "zh"):
            r = convert_file(rel, lang)
            print(r)


if __name__ == "__main__":
    main()
