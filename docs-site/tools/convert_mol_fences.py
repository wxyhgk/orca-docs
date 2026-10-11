#!/usr/bin/env python3
"""Convert ORCA / xyz code fences in tutorial markdown to ```mol panels."""
from __future__ import annotations

import re
from pathlib import Path

FENCE = re.compile(r"(?P<pre>^```)(?P<lang>[\w+-]*)[ \t]*\n(?P<body>.*?)(?P=pre)[ \t]*$", re.M | re.S)

COORD = re.compile(r"^\s*([A-Za-z]{1,3})\s+([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)\s+([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)\s+([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)\s*$")
XYZ_HEAD = re.compile(r"^\s*(\d+)\s*$")


def split_orca_xyz(code: str) -> tuple[str, str]:
    """Return (full_input, xyz_block_or_empty) from ORCA input text."""
    lines = code.splitlines()
    xyz_lines: list[str] = []
    charge_mult = "0 1"
    i = 0
    n = len(lines)
    while i < n:
        m = re.match(r"^\s*\*\s*xyz\s+(-?\d+)\s+(\d+)", lines[i], re.I)
        if m:
            charge_mult = f"{m.group(1)} {m.group(2)}"
            i += 1
            while i < n and lines[i].strip() != "*":
                if lines[i].strip():
                    xyz_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1  # skip closing *
            continue
        i += 1
    if not xyz_lines:
        return code.strip(), ""
    # ensure at least one real coord
    coords = [l for l in xyz_lines if COORD.match(l)]
    if not coords:
        return code.strip(), ""
    xyz = f"{len(coords)}\nfrom ORCA input ({charge_mult})\n" + "\n".join(coords)
    return code.strip(), xyz


def standalone_xyz(body: str) -> str | None:
    lines = body.splitlines()
    if not lines:
        return None
    m = XYZ_HEAD.match(lines[0])
    if not m:
        # maybe already coords-only
        coords = [l for l in lines if COORD.match(l)]
        if len(coords) >= 3 and len(coords) >= len(lines) - 2:
            return f"{len(coords)}\nstructure\n" + "\n".join(coords)
        return None
    count = int(m.group(1))
    if count <= 0 or count > 5000:
        return None
    comment = lines[1] if len(lines) > 1 else "structure"
    coords = []
    for l in lines[2:]:
        if COORD.match(l):
            coords.append(l)
    if len(coords) < max(1, min(count, 3)) and len(coords) < 1:
        return None
    if not coords:
        return None
    # if declared count is wildly wrong, trust actual coords
    if abs(len(coords) - count) > 0 and len(coords) != count:
        count = len(coords)
    return f"{count}\n{comment}\n" + "\n".join(coords)


def is_orca(code: str) -> bool:
    head = code.lstrip()
    if head.startswith(("!", "%")):
        return True
    return bool(re.search(r"^\s*\*", code, re.M)) and bool(re.search(r"^\s*[!*%]", code, re.M))


def classify_body(body: str) -> str:
    if "```" in body:  # nested, skip
        return "skip"
    stripped = body.strip()
    if not stripped:
        return "empty"
    if stripped.startswith("title:") or "--- xyz ---" in body or "--- input ---" in body:
        return "already_mol"
    # shell / generic
    if re.search(r"^\s*(mkdir|cd |export |orca |orca_|python|pip |wget |curl |New-Item|set )", body, re.M):
        return "shell"
    if is_orca(body):
        return "orca"
    if standalone_xyz(body):
        return "xyz"
    return "other"


def to_mol(body: str, page_stem: str, idx: int) -> str | None:
    kind = classify_body(body)
    if kind == "orca":
        inp, xyz = split_orca_xyz(body)
        # require coordinates — otherwise leave as a normal code block
        if not xyz:
            return None
        parts = [f"title: {page_stem} #{idx}"]
        parts += ["--- xyz ---", xyz]
        parts += ["--- input ---", inp]
        return "```mol\n" + "\n".join(parts) + "\n```"
    if kind == "xyz":
        xyz = standalone_xyz(body)
        if not xyz:
            return None
        return f"```mol\ntitle: {page_stem} #{idx}\n--- xyz ---\n{xyz}\n```"
    return None


def convert_file(path: Path) -> int:
    text = path.read_text()
    if "```mol" not in text and "```" not in text:
        return 0
    page_stem = path.stem
    counter = [0]
    changed = [0]

    def repl(m: re.Match) -> str:
        lang = m.group("lang") or ""
        body = m.group("body")
        if lang == "mol":
            return m.group(0)
        # only convert bare / text / empty fences (not bash, python, etc.)
        if lang not in ("", "text", "inp", "orca", "xyz"):
            return m.group(0)
        counter[0] += 1
        out = to_mol(body, page_stem, counter[0])
        if out:
            changed[0] += 1
            return out
        return m.group(0)

    new = FENCE.sub(repl, text)
    if new != text:
        path.write_text(new)
    return changed[0]


def main() -> None:
    roots = [
        Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs/en"),
        Path("/Users/wxyhgk/Documents/Quamtum_Chemistry_md/orca/docs-site/docs/zh"),
    ]
    total = 0
    for root in roots:
        sub = 0
        for p in sorted(root.rglob("*.md")):
            n = convert_file(p)
            if n:
                print(f"  {p.relative_to(root)}: {n}")
                sub += n
        print(f"{root.name}: converted {sub}")
        total += sub
    print(f"TOTAL: {total}")


if __name__ == "__main__":
    main()
