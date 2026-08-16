#!/usr/bin/env python3
"""Syntax-check the app's JavaScript. Run before publishing anything.

Structural greps do not catch a broken string literal; only a parser does.
Uses node --check when available, then a light DOM/asset sanity pass.
"""
import re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    errs = []

    node = shutil.which("node") or "/opt/node22/bin/node"
    scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S)
    if not scripts:
        errs.append("no inline <script> found")
    if Path(node).exists():
        for i, js in enumerate(scripts):
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                             encoding="utf-8") as t:
                t.write(js); tmp = t.name
            r = subprocess.run([node, "--check", tmp],
                               capture_output=True, text=True)
            Path(tmp).unlink()
            if r.returncode:
                head = [l for l in r.stderr.splitlines() if l.strip()][:6]
                errs.append(f"script #{i+1} is not valid JS:\n    "
                            + "\n    ".join(head))
    else:
        errs.append("node not found — JS was NOT syntax checked")

    for tag in ("<style>", "</style>", "</script>"):
        if tag not in html:
            errs.append(f"missing {tag}")
    ids = set(re.findall(r"\bid=\"([\w-]+)\"", html))
    for ref in set(re.findall(r"\$\('#([\w-]+)'\)", html)):
        if ref not in ids:
            errs.append(f"$('#{ref}') has no matching element")
    for key in set(re.findall(r"audio:'(\w+)'", html)):
        if not re.search(rf"\b{key}\s*:", html):
            errs.append(f"audio key '{key}' is never defined")
    return errs


def main() -> int:
    targets = [Path(a) for a in sys.argv[1:]] or \
              [ROOT / "app" / "index.html", ROOT / "docs" / "index.html",
               ROOT / "build" / "heaviness.html"]
    bad = 0
    for t in targets:
        if not t.exists():
            print(f"  skip   {t} (not built)"); continue
        errs = check(t)
        print(("  FAIL   " if errs else "  ok     ") + str(t))
        for e in errs:
            print("           " + e); bad = 1
    return bad


if __name__ == "__main__":
    sys.exit(main())
