#!/usr/bin/env python3
"""Convert ORCA Manual MyST → MkDocs markdown.

Fixes {literalinclude} by inlining code from the crawled HTML mirror
(same page, nth highlight block).
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from html import unescape

ROOT = Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca")
MANUAL_EN = ROOT / "md/manual/en"
MANUAL_ZH = ROOT / "md/manual/zh"
HTML_MANUAL = ROOT / "crawl/manual"
DOCS = ROOT / "docs-site/docs"

ADMON_MAP = {
    "note": "note", "warning": "warning", "important": "warning",
    "tip": "tip", "hint": "tip", "attention": "warning",
    "caution": "warning", "seealso": "info", "deprecated": "warning",
}


def convert_admonitions(text: str) -> str:
    def repl(m: re.Match) -> str:
        typ = m.group("type").strip()
        title = (m.group("title") or "").strip()
        body = m.group("body").rstrip("\n")
        kind = ADMON_MAP.get(typ, "note")
        indented = "\n".join(("    " + ln) if ln.strip() else "" for ln in body.splitlines())
        head = f'!!! {kind}' + (f' "{title}"' if title else "")
        return f"{head}\n{indented}\n"

    return re.sub(
        r"^:::\{(?P<type>[^}]+)\}[ \t]*(?P<title>[^\n]*)\n(?P<body>.*?)^:::[ \t]*$",
        repl, text, flags=re.M | re.S,
    )


def convert_labels(text: str) -> str:
    return re.sub(
        r"^\((sec:[^)=]+|tab:[^)=]+|fig:[^)=]+|eqn:[^)=]+|eq:[^)=]+|table:[^)=]+|par:[^)=]+)\)[ \t]*=[ \t]*$",
        lambda m: f'<a id="{m.group(1)}"></a>',
        text, flags=re.M,
    )


def convert_roles(text: str) -> str:
    def ref(m: re.Match) -> str:
        inner = m.group(1)
        if "<" in inner and inner.endswith(">"):
            t, _, lab = inner.rpartition("<")
            return f"[{t.strip()}](#{lab[:-1].strip()})"
        return f"[{inner}](#{inner})"

    text = re.sub(r"\{ref\}`([^`]+)`", ref, text)
    text = re.sub(r"\{numref\}`([^`]+)`", ref, text)
    text = re.sub(r"\{cite\}`([^`]+)`", lambda m: f"[{m.group(1)}](bibliography.md)", text)
    text = re.sub(r"\{eq\}`([^`]+)`", lambda m: f"[Eq](#{m.group(1)})", text)
    text = re.sub(r"\{index\}`[^`]*`", "", text)
    text = re.sub(r"\{download\}`([^`]+)`", r"`\1`", text)
    return text


def extract_html_code_blocks(html_path: Path) -> list[str]:
    """Return visible code texts from Sphinx highlight blocks in order."""
    if not html_path.exists():
        return []
    html = html_path.read_text(errors="ignore")
    blocks = []
    # <div class="highlight-orca ..."><div class="highlight"><pre>...
    for m in re.finditer(
        r'<div class="highlight-[^"]*"[^>]*>\s*<div class="highlight">\s*<pre>(.*?)</pre>',
        html,
        re.S,
    ):
        frag = m.group(1)
        # strip tags, unescape
        frag = re.sub(r"<[^>]+>", "", frag)
        blocks.append(unescape(frag))
    return blocks


def convert_literalincludes(text: str, code_blocks: list[str]) -> str:
    """Replace ```{literalinclude} ...``` with fenced code."""
    counter = [0]

    def repl(m: re.Match) -> str:
        header = m.group(1)
        body = m.group(2)
        # path is first token on the directive line (after {literalinclude})
        path = ""
        toks = header.strip().split()
        if toks:
            path = toks[0]
        lang_m = re.search(r":language:\s*(\S+)", header + "\n" + body)
        lang = lang_m.group(1) if lang_m else "text"
        if lang in ("orcainput", "orcainp"):
            lang = "orca"
        # options-only body (typical): no source text
        body_code = body.split("```", 1)[0]
        stripped = "\n".join(
            ln for ln in body_code.splitlines()
            if not re.match(r"^\s*:[a-z]+:", ln)
        ).strip("\n")

        idx = counter[0]
        counter[0] += 1
        code = stripped
        if idx < len(code_blocks):
            code = code_blocks[idx].rstrip("\n")
        elif not code and path:
            code = f"# file: {path}"
        return f"```{lang}\n{code}\n```"

    return re.sub(
        r"```\{literalinclude\}([^\n]*)\n(.*?)```",
        lambda m: repl(m),
        text,
        flags=re.S,
    )


def convert_figures(text: str) -> str:
    def repl(m: re.Match) -> str:
        header, body = m.group(1), m.group(2)
        path = ""
        for ln in header.splitlines():
            s = ln.strip()
            if s and not s.startswith(":"):
                path = s
                break
        alt_m = re.search(r":alt:\s*(.+)", header)
        alt = alt_m.group(1).strip() if alt_m else (Path(path).stem if path else "figure")
        cap = body.split("```", 1)[0].strip()
        name = Path(path).name if path else "figure"
        # from manual/contents/chapter/page.md → images at ../../../images/manual/
        img = f"../../../images/manual/{name}"
        # drop wildcard image names
        if "*" in name:
            return f"*{cap}*" if cap else ""
        out = f"![{alt}]({img})"
        if cap:
            out += f"\n\n*{cap}*"
        return out

    return re.sub(
        r"```\{figure\}([^\n]*)\n(.*?)```",
        repl, text, flags=re.S,
    )


def convert_file(src: Path, dst: Path, html_path: Path) -> None:
    text = src.read_text()
    text = convert_admonitions(text)
    text = convert_labels(text)
    text = convert_roles(text)
    blocks = extract_html_code_blocks(html_path)
    text = convert_literalincludes(text, blocks)
    text = convert_figures(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text)


def copy_images() -> None:
    src_dir = HTML_MANUAL / "_images"
    for locale in ("en", "zh"):
        dst = DOCS / locale / "images" / "manual"
        dst.mkdir(parents=True, exist_ok=True)
        n = 0
        if src_dir.exists():
            for p in src_dir.iterdir():
                if p.is_file():
                    shutil.copy2(p, dst / p.name)
                    n += 1
        print(f"images → docs/{locale}/images/manual: {n}")


def html_for(md_rel: Path) -> Path:
    # contents/foo/bar.md → contents/foo/bar.html
    return HTML_MANUAL / md_rel.with_suffix(".html")


def main() -> None:
    copy_images()
    for locale, root in (("en", MANUAL_EN), ("zh", MANUAL_ZH)):
        if not root.exists():
            continue
        out_root = DOCS / locale / "manual"
        if out_root.exists():
            shutil.rmtree(out_root)
        count = 0
        for p in sorted(root.rglob("*.md")):
            rel = p.relative_to(root)
            convert_file(p, out_root / rel, html_for(rel))
            count += 1
        print(f"{locale}: {count} pages")

    # post-pass: bibliography + image depth
    for locale in ("en", "zh"):
        root = DOCS / locale / "manual"
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            t = p.read_text()
            t = t.replace("](bibliography.md)", "](../../bibliography.md)")
            # contents/x/y.md needs ../../../images/manual/
            t = t.replace("](images/", "](../../../images/manual/")
            t = t.replace("](../../images/manual/", "](../../../images/manual/")
            t = t.replace("](../images/manual/", "](../../../images/manual/")
            p.write_text(t)


if __name__ == "__main__":
    main()
