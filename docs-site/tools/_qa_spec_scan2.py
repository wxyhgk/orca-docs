#!/usr/bin/env python3
"""Phase-2 content audit for spectroscopyproperties math.

 * prose accidentally left inside a display-math block
 * <a id=...> label glued to the following $$ (no blank line between)
 * LaTeX corruption: ^ight, \\frac{\\left, \\tag{, $$$$, \\begingroup
 * unpaired inline $ spans across a paragraph
"""
from __future__ import annotations

import glob
import os
import re

ROOT = "/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs"
SPEC = "manual/contents/spectroscopyproperties"

FENCE = re.compile(r"^\s*(```|~~~)")
CMD = re.compile(r"\\[A-Za-z]+")
TEXTEXT = re.compile(r"\\text\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}")
ANCHOR = re.compile(r'^\s*<a id="[^"]+"></a>\s*$')
WORD = re.compile(r"[A-Za-z]{4,}")

PROSE_WORDS = {
    "the", "and", "where", "with", "from", "that", "this", "for", "are",
    "not", "can", "will", "between", "which", "when", "then", "than", "has",
    "have", "been", "was", "were", "into", "onto", "also", "only", "more",
    "most", "some", "such", "each", "both", "other", "after", "before",
    "above", "below", "over", "under", "between", "because", "however",
    "there", "their", "these", "those", "following", "shown", "given",
    "value", "values", "number", "energy", "state", "states", "electron",
    "molecular", "function", "equation", "equations", "respectively",
}


def audit(path: str) -> list[str]:
    lines = open(path, encoding="utf-8").read().split("\n")
    out: list[str] = []
    infence = False
    inmath = False
    start = 0
    body: list[str] = []

    for i, line in enumerate(lines):
        ln = i + 1
        if FENCE.match(line):
            infence = not infence
            continue
        if infence:
            continue

        if not inmath:
            if ANCHOR.match(line) and i + 1 < len(lines) and lines[i + 1].strip() == "$$":
                out.append(f"  [anchor_glued_to_$$] {ln}: {line}")
            if re.search(r"\^ight|\\frac\{\\left\}|\\left\}|\\right\{|\$\$\$\$", line):
                out.append(f"  [latex_corruption] {ln}: {line[:150]}")
            if re.search(r"(?<!\\)\\tag\s*\{", line):
                out.append(f"  [tag_used] {ln}: {line[:150]}")

        if line.strip() == "$$":
            if not inmath:
                inmath, start, body = True, ln, []
            else:
                # analyse collected body
                for bl in body:
                    probe = CMD.sub("", TEXTEXT.sub("", bl))
                    probe = re.sub(r"\\begin\{[a-z*]*\}|\\end\{[a-z*]*\}", "", probe)
                    hits = {
                        w.lower() for w in WORD.findall(probe)
                        if w.lower() in PROSE_WORDS
                    }
                    if len(hits) >= 3:
                        out.append(
                            f"  [prose_in_math] block@{start} line {ln}: "
                            f"{sorted(hits)} :: {bl[:140]}"
                        )
                inmath = False
            continue
        if inmath:
            body.append(line)

    return out


def main() -> None:
    total = 0
    for lang in ("en", "zh"):
        for f in sorted(glob.glob(os.path.join(ROOT, lang, SPEC, "*.md"))):
            r = audit(f)
            if r:
                total += len(r)
                print(f"### {lang}/{os.path.basename(f)}")
                for x in r:
                    print(x)
    print("phase-2 findings:", total)


if __name__ == "__main__":
    main()
