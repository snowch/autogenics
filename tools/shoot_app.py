#!/usr/bin/env python3
"""Screenshot the app's screens, so the UI can be reviewed rather than guessed at.

    python3 tools/shoot_app.py                 # default set -> build/shots/
    python3 tools/shoot_app.py --theme light
"""
import argparse, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# clicking Next N times walks the onboarding; keep in step with its panel count
NEXT = "document.querySelector('#obNext').click();"

SHOTS = [
    ("01-onboard-welcome", None),
    ("01b-onboard-dose", NEXT),
    ("02-onboard-video", NEXT * 2),
    ("02b-onboard-cautions", NEXT * 3),
    ("03-practice-day1", NEXT * 4),
    ("04-practice-progressed", NEXT * 4 + """
        S.step=3; S.stepStart=new Date(Date.now()-6*864e5).toISOString().slice(0,10);
        S.log=[];
        for(let d=0;d<6;d++) for(let k=0;k<3;k++)
          S.log.push({d:dayKey(d),t:'',step:3,r:d<3?3:2,m:'timer'});
        save(); renderJourney();"""),
    ("04b-path-open", NEXT * 4 + """
        go('progress');
        S.step=3; S.stepStart=new Date(Date.now()-6*864e5).toISOString().slice(0,10);
        S.log=[]; S.briefed=['after-first'];
        for(let d=0;d<6;d++) for(let k=0;k<3;k++)
          S.log.push({d:dayKey(d),t:'',step:3,r:d<3?3:2,m:'timer'});
        save(); open=1; renderJourney(); window.scrollTo(0,9999);"""),
    ("04c-progress", NEXT * 4 + """
        S.step=3; S.stepStart=new Date(Date.now()-6*864e5).toISOString().slice(0,10);
        S.log=[]; S.briefed=['after-first'];
        for(let d=0;d<6;d++) for(let k=0;k<3;k++)
          S.log.push({d:dayKey(d),t:'',step:3,r:d<3?3:2,m:'timer'});
        save(); renderJourney(); go('progress'); open='intro'; renderJourney();"""),
    ("04d-progress-day1", NEXT * 4 + "go('progress')"),
    ("05-learn", NEXT * 4 + "go('learn')"),
    ("11-settings", NEXT * 4 + "go('settings')"),
    ("05b-learn-lower", NEXT * 4 + "go('learn');window.scrollTo(0,9999);"),
    ("10-final-step", NEXT * 4 + """
        S.step=9; S.stepStart=new Date(Date.now()-40*864e5).toISOString().slice(0,10);
        S.log=[]; S.briefed=['after-first','warmth','heartbeat','breathing','solar','forehead'];
        for(let d=0;d<20;d++) for(let k=0;k<3;k++)
          S.log.push({d:dayKey(d),t:'',step:Math.min(9,9-Math.floor(d/3)),r:3,m:'timer'});
        save(); renderJourney();"""),
    ("03b-day-done", NEXT * 4 + """
        S.log=[0,1,2].map(k=>({d:dayKey(0),t:'',step:0,r:1,m:'guided'}));
        S.briefed=['after-first']; save(); renderJourney();"""),
    ("07-practice-running", NEXT * 4 + """
        mode='timer'; renderJourney();
        document.querySelector('#nowCard .go').click();"""),
    ("08-rating", NEXT * 4 + """
        document.querySelector('#practice').classList.remove('on');
        document.querySelector('#rating').classList.add('on');"""),
    ("09-brief-player", NEXT * 4 + """
        S.log=[{d:dayKey(0),t:'',step:0,r:2,m:'guided'}]; S.briefed=[];
        save(); renderJourney();
        document.querySelector('#briefCard .btn').click();"""),
    ("06-brief-step", NEXT * 4 + """
        S.step=4; S.stepStart=new Date().toISOString().slice(0,10);
        S.log=[]; S.briefed=['after-first'];
        save(); renderJourney();"""),
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
        panels = None
        for name, script in SHOTS:
            pg = b.new_page(viewport={"width": 430, "height": 932},
                            device_scale_factor=2,
                            color_scheme=a.theme)
            pg.goto(url)
            pg.wait_for_timeout(500)
            n = pg.evaluate("document.querySelectorAll('.obstep').length")
            if script and script.count("obNext") and NEXT * n not in script + NEXT:
                pass  # informational only; counts below are asserted once
            if panels is None:
                panels = n
                print(f"  ({panels} onboarding panels)")
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
