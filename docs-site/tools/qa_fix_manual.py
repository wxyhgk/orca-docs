#!/usr/bin/env python3
"""QA-fix ORCA manual markdown for MkDocs rendering.

Fixes in docs/{en,zh}/manual/contents/{7 target dirs}:
  1. Figure-admonitions `!!! note "../../images/NAME.*"` -> real images at
     ../../../images/manual/NAME.ext (wildcard resolved against assets).
  2. Sphinx option/field lines (:width: :class: :header-rows: :subcaptions:
     :class-grid:) left over from directive conversion -> removed.
  3. Mashed captions `*:width: NN%\\nCAP*` -> `*CAP*`.
  4. Leftover table-span roles {cspan}`N` / {rspan}`N` -> stripped.
  5. Image paths ../../images/NAME(.*) -> ../../../images/manual/NAME.ext.
  6. Broken fences: ` ``` --> ` leftover HTML-comment tails; unclosed EOF fence.

Keeps code block bodies and <a id=...> labels. Does not translate.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs")
DIRS = [
    "structurereactivity",
    "moleculardynamics",
    "multiscalesimulations",
    "workflowsautomatization",
    "utilitiesvisualization",
    "orcaarchitecture",
    "appendix",
]

FIELD_RE = re.compile(
    r"^[ \t]*:(?:width|class|header-rows|subcaptions|class-grid|align|scale"
    r"|name|alt|figwidth|figclass|option):[^\n]*$"
)
SPAN_ROLE_RE = re.compile(r"\{(?:cspan|rspan)\}`[^`]*`")
FIG_NOTE_RE = re.compile(r'^!!! note "(?P<path>\.\./\.\./images/[^"]+)"[ \t]*$')
IMG_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)")
FENCE_RE = re.compile(r"^([ \t]*)(`{3,})(.*)$")

report: dict[str, list[str]] = {}


def note(path: Path, msg: str) -> None:
    report.setdefault(str(path), []).append(msg)


def resolve_image(lang: str, name: str) -> str | None:
    """Resolve image basename (possibly with *) to a real file in images/manual."""
    manual = ROOT / lang / "images" / "manual"
    if not name or "*" not in name:
        cand = manual / name
        return name if cand.exists() else None
    stem = name.split("*")[0]
    matches = sorted(
        p.name for p in manual.iterdir() if p.is_file() and p.name.startswith(stem)
    )
    # prefer exact stem + single extension
    exact = [m for m in matches if m.startswith(stem) and m[len(stem) :].count(".") == 1]
    if exact:
        return exact[0]
    return matches[0] if matches else None


def is_in_fence(lines: list[str], idx: int) -> bool:
    """True if 0-based idx sits inside a fenced code block."""
    stack: list[tuple[int, int, str]] = []
    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if m:
            marker, rest = m.group(2), m.group(3).strip()
            if not stack:
                stack.append((i, len(marker), rest))
            else:
                oi, om, orest = stack[-1]
                if rest == "" and marker[0] == "`" and len(marker) >= om:
                    stack.pop()
                else:
                    stack.append((i, len(marker), rest))
        if i == idx:
            return bool(stack)
    return False


def fix_figure_admonitions(text: str, lang: str) -> str:
    """Convert `!!! note "../../images/NAME"` blocks into real markdown images."""
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    changed = 0
    while i < len(lines):
        m = FIG_NOTE_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        raw_path = m.group("path")
        fname = raw_path.split("/")[-1]
        # collect admonition body (indented lines, allowing blank lines)
        j = i + 1
        body: list[str] = []
        while j < len(lines):
            ln = lines[j]
            if ln.strip() == "":
                # blank line: part of body only if next non-blank is indented
                k = j + 1
                while k < len(lines) and lines[k].strip() == "":
                    k += 1
                if k < len(lines) and (lines[k].startswith("    ") or lines[k].startswith("\t")):
                    body.append(ln)
                    j += 1
                    continue
                break
            if ln.startswith("    ") or ln.startswith("\t"):
                body.append(ln[4:] if ln.startswith("    ") else ln[1:])
                j += 1
                continue
            break
        # strip option lines and leading/trailing blanks from body
        caption_lines = [ln for ln in body if not FIELD_RE.match(ln)]
        while caption_lines and caption_lines[0].strip() == "":
            caption_lines.pop(0)
        while caption_lines and caption_lines[-1].strip() == "":
            caption_lines.pop()
        caption = "\n".join(caption_lines).strip()
        resolved = resolve_image(lang, fname)
        if resolved is None:
            # drop wildcard/missing image, keep caption only (convert_figures rule)
            if caption:
                out.append(f"*{caption}*")
                out.append("")
                note(str(raw_path), f"figure image dropped (unresolved): {raw_path}")
            else:
                note(str(raw_path), f"figure block dropped (unresolved, no caption): {raw_path}")
            changed += 1
            i = j
            continue
        alt = Path(resolved).stem
        img = f"![{alt}](../../../images/manual/{resolved})"
        if caption:
            out.append(img)
            out.append("")
            out.append(f"*{caption}*")
        else:
            out.append(img)
        out.append("")
        changed += 1
        i = j
    if changed:
        return "\n".join(out)
    return text


def fix_field_lines(text: str) -> str:
    lines = text.split("\n")
    out = []
    changed = 0
    for i, ln in enumerate(lines):
        if FIELD_RE.match(ln) and not is_in_fence(lines, i):
            changed += 1
            continue
        out.append(ln)
    return "\n".join(out) if changed else text


def fix_span_roles(text: str) -> str:
    new = SPAN_ROLE_RE.sub("", text)
    return new


def fix_mashed_caption(text: str) -> str:
    """*:width: NN%\\nCAPTION*  ->  *CAPTION*  (option line inside italic caption)."""
    return re.sub(r"\*:width:[^\n]*\n\s*", "*", text)


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


def fix_broken_fences(text: str, path: Path) -> str:
    lines = text.split("\n")
    changed = 0
    # 1) closing fence with trailing ` -->` — strip the tail. If that `-->`
    #    closed an HTML comment, also uncomment its opener (fences inside
    #    HTML comments are still parsed by superfences, so a commented-out
    #    code block is always partially visible; keep the code and make the
    #    whole block well-formed).
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
        # remove the matching unclosed `<!--` opener (uncomment the block)
        openers = []
        for i, ln in enumerate(lines):
            if "<!--" in ln and "-->" not in ln:
                openers.append(i)
        if openers:
            oi = openers[-1]
            lines[oi] = lines[oi].replace("<!--", "", 1)
            if lines[oi].strip() == "":
                del lines[oi]
            changed += 1
            note(str(path), f"uncommented block opened at L{oi+1}")
            text2 = "\n".join(lines)

    # 2) unterminated fence at EOF -> close it
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
            oi, om, orest = stack[-1]
            if rest == "" and marker[0] == "`" and len(marker) >= om:
                stack.pop()
            else:
                stack.append((i, len(marker), rest))
    if stack:
        # close with matching backticks at end (before trailing blank/comment lines)
        oi, om, orest = stack[-1]
        end = len(lines)
        while end > oi + 1 and lines[end - 1].strip() == "":
            end -= 1
        insert_at = end
        closer = "`" * om
        lines.insert(insert_at, closer)
        changed += 1
        note(str(path), f"unclosed fence from L{oi+1} closed at L{insert_at+1}")
        text2 = "\n".join(lines)

    return text2 if changed else text


def process_file(path: Path, lang: str) -> None:
    orig = path.read_text(encoding="utf-8")
    text = orig
    # fences first so later passes can see true code-block boundaries
    text = fix_broken_fences(text, path)
    text = fix_figure_admonitions(text, lang)
    text = fix_field_lines(text)
    text = fix_span_roles(text)
    text = fix_mashed_caption(text)
    text = fix_inline_images(text, lang)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        note(str(path), "updated")
    else:
        note(str(path), "no change")


def main() -> None:
    for lang in ("en", "zh"):
        for d in DIRS:
            dirp = ROOT / lang / "manual" / "contents" / d
            if not dirp.exists():
                continue
            for f in sorted(dirp.glob("*.md")):
                process_file(f, lang)
    # print report
    for path, msgs in sorted(report.items()):
        if msgs != ["no change"]:
            print(f"{path}:")
            for msg in msgs:
                print(f"  - {msg}")


if __name__ == "__main__":
    main()
