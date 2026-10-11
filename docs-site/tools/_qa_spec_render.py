#!/usr/bin/env python3
"""Render every spectroscopyproperties page with the exact MkDocs extension
set and report rendering residue:
  * literal $$ surviving outside HTML comments
  * $$..$$ openers in source that produced no <div class="arithmatex">
  * orphan/unclosed code fences
  * headings swallowed by an unclosed HTML comment
"""
from __future__ import annotations

import glob
import os
import re

import markdown

ROOT = "/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs"
SPEC = "manual/contents/spectroscopyproperties"

EXTS = [
    "admonition", "pymdownx.details", "pymdownx.superfences",
    "pymdownx.highlight", "pymdownx.inlinehilite", "pymdownx.snippets",
    "pymdownx.tabbed", "pymdownx.arithmatex", "tables", "footnotes",
    "attr_list", "md_in_html", "toc",
]
CONF = {
    "pymdownx.arithmatex": {"generic": True},
    "pymdownx.tabbed": {"alternate_style": True},
    "pymdownx.highlight": {"anchor_linenums": True},
}

FENCE = re.compile(r"^\s*(```|~~~)")
COMMENT = re.compile(r"<!--.*?-->", re.S)
STRAY_DOLLAR = re.compile(r"\$\$")
ARITH = re.compile(r'<div class="arithmatex">')


def one(src: str) -> tuple[str, int, int]:
    md = markdown.Markdown(extensions=EXTS, extension_configs=CONF)
    html = md.convert(src)
    return html, len(ARITH.findall(html)), src.count("$$\n") // 1


def main() -> None:
    problems = 0
    for lang in ("en", "zh"):
        for f in sorted(glob.glob(os.path.join(ROOT, lang, SPEC, "*.md"))):
            src = open(f, encoding="utf-8").read()
            html, n_arith, _ = one(src)

            # source display openers (solo $$ lines), fences excluded
            infence = False
            openers = 0
            for line in src.split("\n"):
                if FENCE.match(line):
                    infence = not infence
                    continue
                if not infence and line.strip() == "$$":
                    openers += 1
            openers //= 2

            issues = []
            stripped = COMMENT.sub("", html)
            for m in STRAY_DOLLAR.finditer(stripped):
                issues.append(f"literal $$ at {m.start()}: "
                              f"{stripped[max(0, m.start()-70):m.start()+70]!r}")
            if n_arith != openers:
                issues.append(f"math divs {n_arith} != source blocks {openers}")
            if "```" in stripped:
                issues.append("literal ``` in output")
            # fence pairing: source fence pairs vs rendered highlight blocks
            naive, infence, st0 = 0, False, 0
            indents = []
            for line in src.split("\n"):
                if re.match(r"^\s*(```|~~~)", line):
                    indents.append(len(line) - len(line.lstrip()))
                    if not infence:
                        infence, st0 = True, 1
                    else:
                        infence = False
                        naive += 1
            n_blocks = html.count('<div class="highlight"')
            if n_blocks != naive:
                issues.append(f"code blocks rendered {n_blocks} != source pairs {naive}")
            # opener/closer indent mismatch
            for k in range(0, len(indents) - 1, 2):
                if indents[k] != indents[k + 1]:
                    issues.append(
                        f"fence indent mismatch: opener {indents[k]}sp vs closer {indents[k+1]}sp"
                    )
            # headings: source H2/H3 vs html h2/h3
            h_src = len(re.findall(r"^#{2,3} ", src, re.M))
            h_out = len(re.findall(r"<h[23][^>]*>", html))
            if h_out < h_src:
                issues.append(f"headings src {h_src} > out {h_out} (swallowed?)")

            if issues:
                problems += len(issues)
                print(f"### {lang}/{os.path.basename(f)}")
                for i in issues[:8]:
                    print("   ", i)
                if len(issues) > 8:
                    print(f"    ... +{len(issues)-8} more")
    print("render problems:", problems)


if __name__ == "__main__":
    main()
