#!/usr/bin/env python3
"""Scan ORCA manual structurereactivity chapter for MyST/render format defects."""
import re, sys, os

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
FILES = ["index_structurereactivity", "docker", "goat", "mecp", "neb", "solvator",
         "thermochemistry", "conicalintersections", "irc", "optimizations",
         "optimizations_TS", "optimizations_scans"]

LATEX_JUNK = re.compile(r'\\begingroup|\\endgroup|\\footnotesize|\\scriptsize|\\textwidth|\\centering|\^ight|\\frac\{\\left')
MYST_DIR = re.compile(r'(?<![A-Za-z\\])\{(?:option|ref|doc|eq|file|command|numref|code-ref|literalinclude|include|toctree|index|only|eval-rst|raw|figure|note|warning|important|hint|tip|grid|list-table|csv-table|dropdown|tab-set|tab|compactlist)\}')


def scan(path):
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    out = []
    fence_re = re.compile(r'^(\s*)(`{3,})(.*)$')
    in_fence = None
    fence_start = 0
    fence_body = []
    for i, ln in enumerate(lines, 1):
        m = fence_re.match(ln)
        if m:
            ticks, rest = m.group(2), m.group(3).strip()
            if in_fence is None:
                in_fence = ticks
                fence_start = i
                fence_body = []
                if rest.startswith('{'):
                    out.append((i, "MYST-FENCE", ln))
            else:
                body = '\n'.join(fence_body)
                if not body.strip():
                    out.append((fence_start, "EMPTY-FENCE", f"empty body, closes L{i}"))
                if rest and not rest.startswith('```'):
                    out.append((i, "FENCE-CLOSE-WITH-TEXT", ln))
                in_fence = None
            continue
        if in_fence is not None:
            fence_body.append(ln)
            continue
        if re.match(r'^\s*:::+', ln):
            out.append((i, "CONTAINER", ln))
        if re.match(r'^\s*:[\w-]+:', ln):
            out.append((i, "OPTION-LINE", ln))
        if re.search(r'\([A-Za-z][\w.:-]*\)=\s*$', ln) or re.match(r'^\([A-Za-z][\w.:-]*\)=', ln.strip()):
            out.append((i, "MYST-LABEL", ln))
        if MYST_DIR.search(ln):
            out.append((i, "MYST-DIRECTIVE", ln))
        if re.match(r'^\s*\* -', ln):
            out.append((i, "STAR-DASH-ROW", ln))
        if LATEX_JUNK.search(ln):
            out.append((i, "LATEX-JUNK", ln.strip()[:160]))
        if re.search(r'```[A-Za-z][A-Za-z0-9_+-]*```', ln):
            out.append((i, "INLINE-TRIPLETICK", ln))
        if '```' in ln:
            out.append((i, "MIDLINE-TICKS", ln.strip()[:160]))
        for mm in re.finditer(r'\bsec:[A-Za-z][\w.]*', ln):
            s0 = mm.start()
            before = ln[:s0]
            if before.endswith('](') or before.endswith('#') or before.endswith('"') or before.endswith('='):
                continue
            if '<a id=' in before or '<a href=' in before:
                continue
            if re.search(r'\[[^\]]*$', before):
                out.append((i, "SEC-LINKTEXT", ln.strip()[:200]))
            else:
                out.append((i, "BARE-SEC", ln.strip()[:200]))
            break
        dollars = ln.count('$') - ln.count('\\$') * 2
        stripped = ln.strip()
        if '$$' not in stripped and dollars % 2 == 1:
            out.append((i, "ODD-DOLLAR", stripped[:160]))
        if re.search(r'\$\$.+\$\$', stripped) and '```' not in ln:
            out.append((i, "INLINE-DBL", stripped[:160]))
        if re.search(r'(?<!\$)\$[ \t]+\$(?!\$)', stripped) and '$$' not in stripped:
            out.append((i, "EMPTY-MATH", stripped[:160]))
        if re.search(r'\$\$\s*\(\(?', ln) or re.search(r'\$\$.*\)\s*$', ln) and re.search(r'\(\w+[:.\w]*\)', ln):
            out.append((i, "CLOSURE-LABEL", stripped[:160]))
    if in_fence is not None:
        out.append((fence_start, "UNCLOSED-FENCE", f"opened L{fence_start}, never closed"))
    # display math paragraph hygiene
    i = 0
    while i < len(lines):
        ln = lines[i]
        if re.match(r'^(\s*)\$\$$', ln):
            ind = re.match(r'^(\s*)\$\$', ln).group(1)
            if ind:
                out.append((i + 1, "INDENTED-$$", repr(ln)))
            if i > 0 and lines[i-1].strip() and not re.match(r'^\s*`{3,}', lines[i-1]) and lines[i-1].strip() != '$$':
                out.append((i + 1, "NO-BLANK-BEFORE-$$", repr(lines[i-1])[:120]))
            # find closer
            j = i + 1
            while j < len(lines) and not re.match(r'^\s*\$\$', lines[j]):
                if not lines[j].strip() and j > i:
                    out.append((j + 1, "BLANK-INSIDE-$$", f"block opened L{i+1}"))
                j += 1
            if j >= len(lines):
                out.append((i + 1, "UNCLOSED-$$", ""))
                break
            if j + 1 < len(lines) and lines[j+1].strip() and not lines[j+1].startswith('#'):
                out.append((j + 1, "NO-BLANK-AFTER-$$", repr(lines[j+1])[:120]))
            i = j + 1
            continue
        i += 1
    text = '\n'.join(lines)
    for mm in re.finditer(r'^\$\$[^\n]*\n[^\n]*\n\$\$\s*\([^)\n]+\)\s*$', text, re.M):
        line_no = text[:mm.start()].count('\n') + 1
        out.append((line_no, "AFTER-CLOSER-LABEL", mm.group(0).replace('\n', '\\n')[:120]))
    # $$ block paragraph hygiene: opener/closer must be at col 0, blank line separation
    inf = False
    nfence = []
    for ln in lines:
        if re.match(r'^\s*`{3,}', ln):
            inf = not inf
            continue
        if not inf:
            nfence.append(ln)
    body = '\n'.join(nfence)
    n = len(re.findall(r'(?<!\$)\$\$(?!\$)', body))
    if n % 2 != 0:
        out.append((0, "UNPAIRED-$$", f"count={n}"))
    # display $$ opener not at column 0
    for i, ln in enumerate(lines, 1):
        if re.match(r'^\s+\$\$\s*$', ln):
            out.append((i, "INDENTED-$$", repr(ln)))
        if re.search(r'(?<!\$)\$\$(?!\$).*\S', ln) and not ln.strip().startswith('$$'):
            out.append((i, "DBL-MIDLINE", ln.strip()[:160]))
    return out


def main():
    total = 0
    for lang in ('en', 'zh'):
        for name in FILES:
            path = os.path.join(BASE, lang, 'manual/contents/structurereactivity', name + '.md')
            if not os.path.exists(path):
                print(f"MISSING {path}")
                continue
            res = scan(path)
            if res:
                total += len(res)
                print(f"== {lang}/{name}.md ({len(res)})")
                for ln, kind, txt in res:
                    print(f"  {kind} L{ln}: {txt}")
    print(f"TOTAL {total}")


main()
