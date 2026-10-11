#!/usr/bin/env python3
"""Format/math QA scanner for spectroscopyproperties (MkDocs + arithmatex).

Checks, all outside fenced code blocks:
  myst_fence / myst_container / myst_option / myst_role / myst_label
  begingroup  (raw LaTeX sizing wrappers)
  star_dash   (MyST list-table residue  "* - ...")
  bare_sec    (unlinked sec: reference)
  eq_label_after_closer   ($$ ... $$ (label))
  $$  structure:  opener must be col 0 + blank line before, closer must be
      last line of its block (blank line after), no blank inside, balanced
  empty_fence  (``` immediately followed by ``` )
  odd inline $ (after stripping code spans and escaped dollars)
"""
from __future__ import annotations

import glob
import os
import re
import sys

ROOT = "/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs"
SPEC = "manual/contents/spectroscopyproperties"

RE_MYSTFENCE = re.compile(r"^\s*```[{]")
RE_MYSTCONT = re.compile(r"^\s*:::")
RE_MYSTOPT = re.compile(
    r"^\s*:(language|path|alt|width|height|align|class|name|caption|numbered"
    r"|hide-label|label|no-contents|glob|titlesonly|maxdepth|header-rows"
    r"|stub-columns):"
)
RE_MYSTROLE = re.compile(r"\{(ref|numref|cite|index|eq|doc|raw|eval-rst|toctree)\}`")
RE_MYSTLBL = re.compile(r"^\([A-Za-z0-9_.:+/-]+\)=\s*$")
RE_BEGROUP = re.compile(r"\\(begingroup|endgroup|footnotesize|scriptsize)\b")
RE_STARDASH = re.compile(r"^\*\s+-(\s|$)")
RE_BARESEC = re.compile(r"(?<![\[\(\#\"'])sec:[A-Za-z]")
RE_LABEL_AFTER = re.compile(r"^\s*\$\$.+\((eqn?|eq|sec)[: ]")
RE_FENCE = re.compile(r"^\s*(```|~~~)")
CODESPAN = re.compile(r"`+[^`\n]*`+")


def dollars(s: str) -> int:
    s = CODESPAN.sub("", s).replace("\\$", "")
    c = i = 0
    while i < len(s):
        if s[i] == "$":
            if i + 1 < len(s) and s[i + 1] == "$":
                i += 2
                continue
            c += 1
            i += 1
        else:
            i += 1
    return c


def scan(path: str) -> list[tuple[int, str, str]]:
    lines = open(path, encoding="utf-8").read().split("\n")
    out: list[tuple[int, str, str]] = []
    infence = False
    inmath = False
    math_open = 0
    open_indent = 0
    n = len(lines)

    for idx, line in enumerate(lines):
        ln = idx + 1
        if RE_FENCE.match(line):
            if inmath:
                out.append((math_open, "unclosed_$$", "fence hit while in math"))
                inmath = False
            infence = not infence
            continue
        if infence:
            continue
        s = line.strip()

        for rx, tag in (
            (RE_MYSTFENCE, "myst_fence"),
            (RE_MYSTCONT, "myst_container"),
            (RE_MYSTOPT, "myst_option"),
            (RE_MYSTROLE, "myst_role"),
            (RE_MYSTLBL, "myst_label"),
            (RE_BEGROUP, "latex_begingroup"),
            (RE_STARDASH, "star_dash_row"),
            (RE_BARESEC, "bare_sec"),
            (RE_LABEL_AFTER, "label_after_closer"),
        ):
            if rx.search(line):
                out.append((ln, tag, line[:150]))

        if s == "$$":
            if not inmath:
                open_indent = len(line) - len(line.lstrip())
            elif (len(line) - len(line.lstrip())) != open_indent:
                out.append((ln, "$$_indent_mismatch",
                            f"open {open_indent}sp vs close {len(line)-len(line.lstrip())}sp"))
            if not inmath:
                inmath, math_open = True, ln
                if ln > 1 and lines[idx - 1].strip() != "":
                    out.append((ln, "$$open_prev_not_blank", lines[idx - 1][:90]))
            else:
                inmath = False
                if lines[idx - 1].strip() == "":
                    out.append((ln, "$$close_prev_blank", "empty body"))
                if idx + 1 < n and lines[idx + 1].strip() != "":
                    out.append((ln, "$$close_next_not_blank", lines[idx + 1][:90]))
            continue
        if "$$" in line:
            if inmath:
                out.append((ln, "$$_glued_closer", line[:150]))
                inmath = False
            else:
                out.append((ln, "$$_glued_line", line[:150]))
            continue
        if inmath:
            if s == "":
                out.append((ln, "blank_inside_$$", f"open@{math_open}"))
            continue
        if dollars(line) % 2:
            out.append((ln, "odd_$_count", line[:150]))

    if inmath:
        out.append((math_open, "unclosed_$$", "EOF"))

    for i in range(n - 1):
        if lines[i].strip() == "```" and lines[i + 1].strip() == "```":
            out.append((i + 1, "empty_fence", lines[i]))

    txt = "\n".join(
        l for i, l in enumerate(lines) if not RE_FENCE.match(l)
    )
    return out


def main() -> None:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    bad = 0
    for lang in ("en", "zh"):
        for f in sorted(glob.glob(os.path.join(ROOT, lang, SPEC, "*.md"))):
            name = os.path.basename(f)
            if only and only not in name:
                continue
            r = scan(f)
            if r:
                bad += 1
                print(f"### {lang}/{name}")
                for ln, tag, ctx in r:
                    print(f"   [{tag}] {ln}: {ctx}")
    print(f"files with findings: {bad}")


if __name__ == "__main__":
    main()
