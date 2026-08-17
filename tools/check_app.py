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

    # In a built file the injected map replaces the fallback entirely, so any
    # key the code reads must be present in it. A missing optional key fails
    # silently at runtime — that is how the video shipped without its poster.
    # A local `const go = ...` inside a function shadows the top-level go()
    # navigator for that whole scope, so every call to it from a handler
    # declared there silently returns a DOM element instead of navigating.
    # Valid JavaScript, invisible to node --check, and it shipped once.
    js = "\n".join(scripts)
    top = set(re.findall(r"^function (\w+)\(", js, re.M))
    for name in sorted(top):
        for m in re.finditer(r"\b(?:const|let|var)\s+" + name + r"\s*=", js):
            line = js[:m.start()].count("\n") + 1
            errs.append(f"line {line}: local '{name}' shadows the top-level "
                        f"function {name}() — calls to it in that scope will "
                        f"not do what they look like")

    # Timer mode shows the cue lines on screen while the practitioner says them
    # silently; guided mode plays the recording. If a cue is not a line the
    # recording actually speaks, the two halves of the same step disagree — and
    # editing one without the other is exactly how that happens.
    SCRIPTS = {"s1": "arm-heaviness-example", "s2": "arm-heaviness-example-2",
               "s3": "arm-heaviness-example-3", "legs": "at-heaviness-legs",
               "warmth": "at-warmth", "heartbeat": "at-heartbeat",
               "breathing": "at-breathing", "solar": "at-solar-plexus",
               "forehead": "at-forehead"}
    root = Path(__file__).resolve().parent.parent
    for n, q, aud, cues in re.findall(
            r"\{n:'([^']+)', q:'([^']*)'.*?audio:(null|'[a-z0-9]+').*?cues:\[(.*?)\]\}",
            html, re.S):
        key = aud.strip("'")
        if key == "null":
            continue
        src = root / "script" / (SCRIPTS.get(key, "") + ".md")
        if not src.exists():
            errs.append(f"step {n} names audio '{key}' with no script to check it against")
            continue
        body = src.read_text(encoding="utf-8")
        body = body.split("<!-- narration:start -->")[1].split("<!-- narration:end -->")[0]
        spoken = {re.sub(r"\s+", " ", ln).strip() for ln in body.splitlines()
                  if ln.strip() and not ln.startswith(("[", "#"))}
        for cue in {c.strip().strip("'") for c in cues.split(",")}:
            if cue not in spoken:
                errs.append(f"step '{n} — {q}': the on-screen cue {cue!r} is "
                            f"never spoken in {src.name}")

    # Reset promises "start again from the beginning". It once set
    # onboarded:true, which reset the record but skipped first run entirely.
    rst = re.search(r"lReset'\)\.onclick[\s\S]*?S=\{(.*?)\};", html)
    fresh = re.search(r"return \{(step:0[^}]*)\};", html)
    if rst and fresh:
        rkeys = set(re.findall(r"(\w+)\s*:", rst.group(1)))
        fkeys = set(re.findall(r"(\w+)\s*:", fresh.group(1)))
        if "onboarded:false" not in rst.group(1).replace(" ", ""):
            errs.append("reset does not clear onboarded — first run will not "
                        "re-appear, so 'start again from the beginning' lies")
        missing = fkeys - rkeys
        if missing:
            errs.append("reset omits state key(s) present on a fresh install: "
                        + ", ".join(sorted(missing)) + " — stale data survives a reset")
    else:
        errs.append("could not find the reset handler or the fresh-install state")

    m = re.search(r"window\.__AUDIO__=\{(.*?)\n\};", html, re.S)
    if m:
        injected = set(re.findall(r"(\w+)\s*:", m.group(1)))
        for key in sorted(set(re.findall(r"\bAUDIO\.(\w+)\b", html))):
            if key not in injected:
                errs.append(f"AUDIO.{key} is read but missing from the "
                            f"injected map — it will be undefined at runtime")
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
