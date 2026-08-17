#!/usr/bin/env python3
"""Screenshot the app's screens, so the UI can be reviewed rather than guessed at.

    python3 tools/shoot_app.py                 # default set -> build/shots/
    python3 tools/shoot_app.py --theme light
"""
import argparse, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

SHOTS = [
    ("01-onboard-safety", None),
    ("02-onboard-video", "document.querySelector('#obNext').click()"),
    ("03-practice", "document.querySelector('#obNext').click();"
                    "document.querySelector('#obNext').click()"),
    ("04-practice-progressed", """
        document.querySelector('#obNext').click();
        document.querySelector('#obNext').click();
        S.step=3; S.stepStart=new Date(Date.now()-6*864e5).toISOString().slice(0,10);
        S.log=[];
        for(let d=0;d<6;d++) for(let k=0;k<3;k++)
          S.log.push({d:dayKey(d),t:'',step:3,r:d<3?3:2,m:'timer'});
        save(); renderJourney();"""),
    ("05-learn", "document.querySelector('#obNext').click();"
                 "document.querySelector('#obNext').click();"
                 "go('learn')"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", default="dark", choices=("dark", "light"))
    ap.add_argument("--out", type=Path, default=ROOT / "build" / "shots")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright
    url = (ROOT / "app" / "index.html").as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME,
                              args=["--no-sandbox", "--disable-dev-shm-usage",
                                    "--autoplay-policy=no-user-gesture-required"])
        for name, script in SHOTS:
            pg = b.new_page(viewport={"width": 430, "height": 932},
                            device_scale_factor=2,
                            color_scheme=a.theme)
            pg.goto(url)
            pg.wait_for_timeout(500)
            if script:
                pg.evaluate(script)
                pg.wait_for_timeout(400)
            f = a.out / f"{name}-{a.theme}.png"
            pg.screenshot(path=str(f), full_page=False)
            print(f"  {f.name}")
            pg.close()
        b.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
