"""
MkDocs hook: turn fenced ```mol blocks into 3D | input panels.

```mol
title: Water
theme: chem311
--- xyz ---
3
water
...
--- input ---
!HF DEF2-SVP
* xyz 0 1
...
*
```

Uses on_page_markdown so we do not depend on markdown_extensions registration.
"""
from __future__ import annotations

import html
import re

FENCE = re.compile(
    r"^(?P<indent>[ \t]*)```mol[ \t]*\n(?P<body>.*?)(?:\n(?P=indent)```)[ \t]*$",
    re.M | re.S,
)


def _split_body(source: str) -> tuple[dict[str, str], str, str]:
    meta: dict[str, str] = {}
    xyz_lines: list[str] = []
    inp_lines: list[str] = []
    section = "meta"
    for line in source.splitlines():
        s = line.strip()
        if s in ("--- xyz ---", "---xyz---", "### xyz"):
            section = "xyz"
            continue
        if s in ("--- input ---", "---input---", "--- orca ---", "### input"):
            section = "input"
            continue
        if section == "meta" and re.match(r"^[A-Za-z_][\w-]*\s*:\s*\S", s):
            k, _, v = s.partition(":")
            meta[k.strip().lower()] = v.strip()
            continue
        if section == "meta":
            section = "xyz"
            xyz_lines.append(line)
            continue
        if section == "xyz":
            xyz_lines.append(line)
        else:
            inp_lines.append(line)
    return meta, "\n".join(xyz_lines).strip("\n"), "\n".join(inp_lines).strip("\n")


def render_mol_panel(source: str) -> str:
    meta, xyz, inp = _split_body(source)
    title = meta.get("title", "")
    theme = meta.get("theme", "chem311")
    height = meta.get("height", "360px")
    representation = meta.get("representation", "ball-stick")
    fmt = meta.get("format", "xyz")

    # Normalize xyz: drop blank lines, require non-empty comment (blank
    # comments become an extra empty line after HTML round-trip).
    if xyz:
        raw = [l.rstrip() for l in xyz.splitlines() if l.strip()]
        if raw and re.match(r"^\s*\d+\s*$", raw[0]):
            comment = raw[1] if len(raw) > 1 and not re.match(
                r"^\s*[A-Za-z]{1,3}\s+[-+]?\d", raw[1]
            ) else "structure"
            coords = [l for l in raw if re.match(r"^\s*[A-Za-z]{1,3}\s+[-+]?\d", l)]
            if coords:
                xyz = f"{len(coords)}\n{comment or 'structure'}\n" + "\n".join(coords)
            else:
                xyz = ""

    # No coordinates → do not emit a fast-mol panel
    if not xyz:
        if inp:
            cls = "language-text"
            return f'<pre class="highlight"><code class="{cls}">{html.escape(inp)}</code></pre>'
        return ""

    attrs = [
        'class="mol-panel"',
        f'data-mol-theme="{html.escape(theme, True)}"',
        f'data-mol-height="{html.escape(height, True)}"',
        f'data-mol-repr="{html.escape(representation, True)}"',
    ]
    if title:
        attrs.append(f'data-mol-title="{html.escape(title, True)}"')
    # never insert HTML comments inside <pre> — textContent drops them but
    # keeps surrounding newlines, which corrupts XYZ blank-line layout
    xyz_out = html.escape(xyz)
    inp_out = html.escape(inp)
    return (
        f'<div {" ".join(attrs)}>\n'
        f'<pre class="mol-xyz" data-format="{html.escape(fmt, True)}">{xyz_out}</pre>\n'
        f'<pre class="mol-input">{inp_out}</pre>\n'
        f"</div>"
    )


def _sub_fences(text: str) -> str:
    return FENCE.sub(lambda m: m.group(1) + render_mol_panel(m.group("body")), text)


def on_page_markdown(markdown: str, **kwargs) -> str:
    if "```mol" not in markdown:
        return markdown
    return _sub_fences(markdown)
