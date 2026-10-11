#!/usr/bin/env python3
"""Normalize display-math blocks in spectroscopyproperties for pymdownx.arithmatex.

arithmatex block pattern is  ^$$ ... $$[ ]*$  matched against a Markdown
"block" (a run of lines split on blank lines).  So a display equation only
renders when it is a standalone paragraph at column 0 with:
  * a blank line before the opener and after the closer
  * no blank line inside the block
  * no glued delimiters (``$$body`` / ``body$$``)
  * delimiters not indented

Usage:  python3 qa_fix_spec_math.py [--apply]
"""
from __future__ import annotations

import glob
import os
import re
import sys

ROOT = "/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs"
SPEC = "manual/contents/spectroscopyproperties"

FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})")


def d2(line: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in re.finditer(r"\$\$", line)]


def normalize(text: str) -> tuple[str, dict]:
    lines = text.split("\n")
    out: list[str] = []
    infence = False
    mode = "prose"
    body: list[str] = []
    need_blank = False
    st = {
        "blocks": 0,
        "dropped_empty": 0,
        "inline_to_single": 0,
        "split_single_line": 0,
        "glued": 0,
        "blank_inside": 0,
    }

    def ensure_blank() -> None:
        if out and out[-1] != "":
            out.append("")

    def emit_prose(line: str) -> None:
        nonlocal need_blank
        if need_blank:
            if line.strip() != "":
                out.append("")
            need_blank = False
        out.append(line)

    def flush(body_lines: list[str]) -> None:
        nonlocal need_blank
        while body_lines and body_lines[-1].strip() == "":
            body_lines.pop()
        ensure_blank()
        out.append("$$")
        out.extend(body_lines)
        out.append("$$")
        st["blocks"] += 1
        need_blank = True

    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if FENCE_RE.match(line):
            if mode == "math":
                flush(body)
                body = []
                mode = "prose"
            infence = not infence
            emit_prose(line)
            i += 1
            continue
        if infence:
            emit_prose(line)
            i += 1
            continue

        if mode == "prose":
            toks = d2(line)
            if not toks:
                emit_prose(line)
                i += 1
                continue

            # stand-alone single-line $$body$$ -> display block
            if (
                len(toks) == 2
                and line[: toks[0][0]].strip() == ""
                and line[toks[1][1] :].strip() == ""
            ):
                inner = line[toks[0][1] : toks[1][0]]
                flush([inner] if inner.strip() else [])
                st["split_single_line"] += 1
                i += 1
                continue

            # $$..$$ embedded in prose -> single-$ inline math
            if len(toks) >= 2 and len(toks) % 2 == 0:
                new = line
                for k in range(len(toks) - 1, -1, -2):
                    a, b = toks[k - 1], toks[k]
                    new = new[: a[0]] + "$" + new[a[1] : b[0]] + "$" + new[b[1] :]
                emit_prose(new)
                st["inline_to_single"] += 1
                i += 1
                continue

            s, e = toks[0]
            before, after = line[:s], line[e:]
            if before.strip():
                emit_prose(before.rstrip())
                st["glued"] += 1
            rest = d2(after)
            if rest:  # region opens and closes on this line
                b2, e2 = rest[0]
                inner, tail = after[:b2], after[e2:]
                if inner.strip():
                    flush([inner])
                    st["glued"] += 1
                else:
                    st["dropped_empty"] += 1
                if tail.strip():
                    emit_prose(tail)
                i += 1
                continue
            mode, body = "math", []
            if after.strip():
                body.append(after)
                st["glued"] += 1
            i += 1
            continue

        # mode == 'math'
        toks = d2(line)
        if toks:
            s, e = toks[0]
            head, tail = line[:s], line[e:]
            if head.strip():
                if line[s:] == "$$" and not body:
                    pass
                body.append(head)
                st["glued"] += 1
            if not any(l.strip() for l in body):
                st["dropped_empty"] += 1
                body = []
            else:
                flush(body)
                body = []
            mode = "prose"
            need_blank = True
            if tail.strip():
                emit_prose(tail)
            i += 1
            continue
        if line.strip() == "":
            st["blank_inside"] += 1
        else:
            body.append(line)
        i += 1

    if mode == "math" and body:
        flush(body)

    return "\n".join(out), st


def main() -> None:
    apply = "--apply" in sys.argv
    total = 0
    for lang in ("en", "zh"):
        for f in sorted(glob.glob(os.path.join(ROOT, lang, SPEC, "*.md"))):
            src = open(f, encoding="utf-8").read()
            new, st = normalize(src)
            if new != src:
                total += 1
                if apply:
                    open(f, "w", encoding="utf-8").write(new)
                print(f"{'CHANGED' if apply else 'would change'} {lang}/{os.path.basename(f)}: {st}")
    print(f"files: {total}")


if __name__ == "__main__":
    main()
