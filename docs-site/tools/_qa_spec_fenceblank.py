#!/usr/bin/env python3
"""Insert a blank line between top-level prose and an adjacent code fence.

A fence opener glued to the previous prose line (or a closer glued to the
following line) makes Python-Markdown fold the fenced block into the same
paragraph, so the emitted <div class="highlight"> ends up nested inside <p>.
Only column-0 fences with column-0 neighbours are touched, so list /
admonition nesting is never altered.  Metrics are checked before/after.
"""
from __future__ import annotations

import glob
import os
import re

ROOT = "docs"
SPEC = "manual/contents/spectroscopyproperties"
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})")


def metrics(src: str) -> tuple:
    """Structural metrics that must not change."""
    import markdown
    EXTS = ["admonition", "pymdownx.details", "pymdownx.superfences", "pymdownx.highlight",
            "pymdownx.inlinehilite", "pymdownx.snippets", "pymdownx.tabbed",
            "pymdownx.arithmatex", "tables", "footnotes", "attr_list", "md_in_html", "toc"]
    CONF = {"pymdownx.arithmatex": {"generic": True},
            "pymdownx.tabbed": {"alternate_style": True},
            "pymdownx.highlight": {"anchor_linenums": True}}
    md = markdown.Markdown(extensions=EXTS, extension_configs=CONF)
    html = md.convert(src)
    import re as _re
    h2 = _re.sub(r"<!--.*?-->", "", html, flags=_re.S)
    return (
        html.count('<div class="highlight"'),
        html.count('<div class="arithmatex">'),
        html.count('<span class="arithmatex">'),
        len(_re.findall(r"<h[1-6][^>]*>", html)),
        "$$" in _re.sub(r"<pre>.*?</pre>", "", h2, flags=_re.S),
        "```" in _re.sub(r"<pre>.*?</pre>", "", h2, flags=_re.S),
        len(_re.findall(r'<p>(?:(?!</p>).)*<div class="highlight">', h2, flags=_re.S)),
    )


def glue(src: str) -> int:
    L = src.split("\n")
    n = 0
    infence = False
    for i, l in enumerate(L):
        m = FENCE.match(l)
        if not m:
            continue
        if not infence:
            if m.group(1) == "" and i > 0 and L[i - 1].strip() and L[i - 1][:1] != " ":
                n += 1
            infence = True
        else:
            if m.group(1) == "" and i + 1 < len(L) and L[i + 1].strip() and L[i + 1][:1] != " ":
                n += 1
            infence = False
    return n


def fix(src: str) -> str:
    L = src.split("\n")
    out: list[str] = []
    infence = False
    for i, l in enumerate(L):
        m = FENCE.match(l)
        if m and m.group(1) == "":
            if not infence:
                if out and out[-1].strip() and out[-1][:1] != " ":
                    out.append("")
                infence = True
            else:
                out.append(l)
                infence = False
                nxt = L[i + 1] if i + 1 < len(L) else ""
                if nxt.strip() and nxt[:1] != " ":
                    out.append("")
                continue
        out.append(l)
    return "\n".join(out)


def main() -> None:
    apply = "--apply" in os.sys.argv
    changed = 0
    for lang in ("en", "zh"):
        for f in sorted(glob.glob(f"{ROOT}/{lang}/{SPEC}/*.md")):
            src = open(f, encoding="utf-8").read()
            g = glue(src)
            if not g:
                continue
            new = fix(src)
            if new == src:
                continue
            before, after = metrics(src), metrics(new)
            ok = before[:6] == after[:6]
            delta = before[6] - after[6]
            tag = "KEEP" if ok else "REJECT"
            if ok and apply:
                open(f, "w", encoding="utf-8").write(new)
                changed += 1
            print(f"{tag} {lang}/{os.path.basename(f)}: glue={g} metrics_ok={ok} "
                  f"p<div> {before[6]}->{after[6]} (removed {delta})")
    print("files changed:", changed if apply else "(dry-run)")


if __name__ == "__main__":
    main()
