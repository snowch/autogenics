#!/usr/bin/env python3
"""Behavioural tests for the step gate — run it, do not read it.

check_app.py catches structural mistakes. It cannot catch a gate that opens
for the wrong reason, because the code parses cleanly either way. This one
loads the real app in a browser and asks gate() what it thinks.

It exists because the floor was measured in calendar days since the step
opened, so *absence counted as practice*: two sessions, three weeks away, then
three good days, and a gate meant to mean "about a week on this phrase" opened
on six days of work spread over twenty-four.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

SEED = """([raw, ago])=>{
  const dk=b=>{const d=new Date(); d.setDate(d.getDate()-b); return d.toISOString().slice(0,10);};
  const log=[];
  raw.forEach(e=>{ for(let i=0;i<e[1];i++) log.push({d:dk(e[0]),t:'',step:0,r:e[2],m:'timer'}); });
  localStorage.setItem('autogenics.v2', JSON.stringify(
    {step:0, log:log, stepStart:dk(ago), onboarded:true,
     warned:[], briefed:['after-first'], theme:'system'}));
}"""

def day(back, times=2, rating=3):
    return [back, times, rating]

# name, log (day-back, practices, rating), days since the step opened, expected
CASES = [
    ("a lapse must not open the gate",
     [day(23), day(2), day(1), day(0)], 24, False),
    ("seven practised days, landing, opens it",
     [day(b) for b in (6, 5, 4, 3, 2, 1, 0)], 7, True),
    ("six practised days is not seven",
     [day(b) for b in (5, 4, 3, 2, 1, 0)], 6, False),
    ("once a day is not evidence",
     [day(b, times=1) for b in (6, 5, 4, 3, 2, 1, 0)], 7, False),
    ("faint ratings are not evidence",
     [day(b, rating=1) for b in (6, 5, 4, 3, 2, 1, 0)], 7, False),
    ("landing must be recent, not historic",
     [day(b) for b in (9, 8, 7, 6, 5, 4)] + [day(b, rating=1) for b in (2, 1, 0)],
     10, False),
]

# practice days already behind you -> should the guided track still be default?
GUIDED = [([], True), ([0], True), ([1, 0], True), ([2, 1, 0], True),
          ([3, 2, 1, 0], False)]


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "app" / "index.html"
    fails, errs = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 390, "height": 844})
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + str(target.resolve()))
        pg.wait_for_timeout(300)

        for name, log, ago, want in CASES:
            pg.evaluate(SEED, [log, ago])
            pg.reload(); pg.wait_for_timeout(200)
            g = pg.evaluate("gate()")
            ok = g["ready"] == want
            print(f'  {"ok  " if ok else "FAIL"}  {name:44s} '
                  f'days={g["days"]:2d} floor={g["floorOk"]:d} evidence={g["evidenceOk"]:d} '
                  f'ready={g["ready"]:d}')
            if not ok:
                fails.append(f"{name}: expected ready={want}")

        for prior, want in GUIDED:
            pg.evaluate(SEED, [[day(b) for b in prior], max(prior) if prior else 0])
            pg.reload(); pg.wait_for_timeout(200)
            got = pg.evaluate("guidedDefault()")
            ok = got == want
            print(f'  {"ok  " if ok else "FAIL"}  guided default after '
                  f'{len(prior)} practised day(s): {got}')
            if not ok:
                fails.append(f"guided after {len(prior)} days: expected {want}")
        b.close()

    if errs:
        fails.append("page errors: " + "; ".join(errs))
    for f in fails:
        print("  FAIL  " + f)
    print("  ok" if not fails else f"  {len(fails)} failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
