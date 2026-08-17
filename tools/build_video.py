#!/usr/bin/env python3
"""Render a narrated video from a script — slides cut to the narration.

Slides are HTML, screenshotted with the pre-installed Chromium, then assembled
against the script's own audio. Because the audio pipeline already knows every
segment's exact duration, cuts land on the narration rather than near it.

    python3 tools/build_video.py script/intro.md --frames    # stills only
    python3 tools/build_video.py script/intro.md             # full mp4
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W, H = 1080, 1350          # 4:5, the shape that fills a phone in a feed

# The container has Bitstream Charter — a real book serif, not a fallback.
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:%dpx;height:%dpx;background:#0D1218;color:#E6ECF2;
  font-family:'Liberation Sans','DejaVu Sans',sans-serif;
  display:flex;flex-direction:column;justify-content:center;
  padding:132px 96px 118px;overflow:hidden;position:relative}
.kick{font-family:'DejaVu Sans Mono',monospace;font-size:26px;letter-spacing:.22em;
  text-transform:uppercase;color:#E0A15C;margin-bottom:34px}
h1{font-family:Charter,'Bitstream Charter',serif;font-weight:400;font-size:92px;
  line-height:1.08;letter-spacing:-.02em;text-wrap:balance}
h1.sm{font-size:70px}
p{font-size:34px;line-height:1.5;color:#9DAEBD;margin-top:34px;max-width:22ch}
.formula{font-family:Charter,'Bitstream Charter',serif;font-size:104px;line-height:1.12;
  color:#E0A15C;letter-spacing:-.02em}
.stats{display:flex;gap:78px;margin-top:56px}
.stats .n{font-family:'DejaVu Sans Mono',monospace;font-size:76px;color:#E0A15C;letter-spacing:-.03em}
.stats .c{font-size:26px;color:#6F8090;margin-top:10px;max-width:9ch;line-height:1.3}
.rule{width:74px;height:3px;background:#E0A15C;margin-bottom:38px}
.bens{margin-top:44px;display:flex;flex-direction:column;gap:26px}
.ben{display:flex;gap:22px;align-items:baseline}
.ben .bm{width:11px;height:11px;border-radius:50%%;background:#E0A15C;flex:none}
.ben .bt{font-size:40px;line-height:1.32;color:#E6ECF2}
.ben .bt i{font-style:normal;color:#6F8090;display:block;font-size:31px;margin-top:6px}
/* graphics reuse the app's own vocabulary, so video and product agree */
.dose{display:flex;gap:22px;margin-top:56px}
.dose .s{flex:1;height:132px;border-radius:20px;border:2px solid #243140;background:#0A0F14;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px}
.dose .s.on{border-color:#E0A15C;background:#332417}
.dose .s .m{font-family:'DejaVu Sans Mono',monospace;font-size:38px;color:#3A4653}
.dose .s.on .m{color:#E0A15C}
.dose .s .l{font-family:'DejaVu Sans Mono',monospace;font-size:20px;letter-spacing:.12em;
  text-transform:uppercase;color:#6F8090}
.ladder{margin-top:48px;display:flex;flex-direction:column;gap:0}
.ladder .r{display:grid;grid-template-columns:34px 1fr;column-gap:24px;align-items:start}
.ladder .rail{display:flex;flex-direction:column;align-items:center;height:100%%}
.ladder .d{width:18px;height:18px;border-radius:50%%;border:3px solid #243140;background:#0D1218;flex:none;margin-top:9px}
.ladder .r.on .d{background:#E0A15C;border-color:#E0A15C;box-shadow:0 0 0 7px #332417}
.ladder .r.past .d{background:#3F7D66;border-color:#3F7D66}
.ladder .ln{width:3px;flex:1;background:#243140;min-height:34px}
.ladder .r.past .ln{background:#3F7D66;opacity:.45}
.ladder .t{font-size:34px;padding-bottom:26px;color:#6F8090}
.ladder .r.on .t{color:#E6ECF2;font-weight:600}
.ladder .r.past .t{color:#9DAEBD}
.arc{margin-top:44px;display:flex;justify-content:center}
.mark{position:absolute;left:96px;bottom:74px;font-family:'DejaVu Sans Mono',monospace;
  font-size:22px;letter-spacing:.2em;text-transform:uppercase;color:#3A4653}
.dots{position:absolute;right:96px;bottom:74px;display:flex;gap:9px}
.dots i{width:9px;height:9px;border-radius:50%%;background:#243140;display:block}
.dots i.on{background:#E0A15C;width:30px;border-radius:5px}
""" % (W, H)


def slide_html(s, idx, total):
    dots = "".join(f'<i class="{"on" if i==idx else ""}"></i>' for i in range(total))
    kind = s.get("kind", "point")
    if kind == "dose":
        cells = "".join(
            f'<div class="s{" on" if i < s.get("filled",0) else ""}">'
            f'<div class="m">{"✓" if i < s.get("filled",0) else "–"}</div>'
            f'<div class="l">{lab}</div></div>'
            for i, lab in enumerate(["Morning", "Midday", "Evening"]))
        body = (f'<div class="kick">{s.get("kick","")}</div><h1 class="sm">{s["text"]}</h1>'
                f'<div class="dose">{cells}</div>')
    elif kind == "ladder":
        rows = ""
        for i, (name, st) in enumerate(s["rows"]):
            last = ' style="min-height:0"' if i == len(s["rows"]) - 1 else ""
            cls = "r on" if st is True or st == "on" else ("r past" if st == "past" else "r")
            rows += (f'<div class="{cls}"><div class="rail"><div class="d"></div>'
                     f'<div class="ln"{last}></div></div><div class="t">{name}</div></div>')
        body = (f'<div class="kick">{s.get("kick","")}</div><h1 class="sm">{s["text"]}</h1>'
                f'<div class="ladder">{rows}</div>')
    elif kind == "arc":
        pct = s.get("pct", 0.62)
        C = 2 * 3.14159 * 150
        body = (f'<div class="kick">{s.get("kick","")}</div><h1 class="sm">{s["text"]}</h1>'
                f'<div class="arc"><svg width="380" height="380" viewBox="0 0 340 340">'
                f'<circle cx="170" cy="170" r="150" fill="none" stroke="#243140" stroke-width="5"/>'
                f'<circle cx="170" cy="170" r="150" fill="none" stroke="#E0A15C" stroke-width="5"'
                f' stroke-linecap="round" stroke-dasharray="{C:.0f}"'
                f' stroke-dashoffset="{C*(1-pct):.0f}" transform="rotate(-90 170 170)"/>'
                f'<text x="170" y="170" text-anchor="middle" dominant-baseline="central"'
                f' font-family="DejaVu Sans Mono" font-size="64" fill="#E6ECF2">{s.get("label","1:36")}</text>'
                f'</svg></div>')
    elif kind == "formula":
        body = f'<div class="rule"></div><div class="formula">{s["text"]}</div>'
    elif kind == "stats":
        cells = "".join(f'<div><div class="n">{n}</div><div class="c">{c}</div></div>'
                        for n, c in s["stats"])
        body = (f'<div class="kick">{s.get("kick","")}</div>'
                f'<h1 class="sm">{s["text"]}</h1><div class="stats">{cells}</div>')
    elif kind == "benefits":
        items = "".join(f'<div class="ben"><span class="bm"></span>'
                        f'<span class="bt">{t}<i>{sub}</i></span></div>'
                        for t, sub in s["items"])
        body = (f'<div class="kick">{s.get("kick","")}</div>'
                f'<h1 class="sm">{s["text"]}</h1><div class="bens">{items}</div>')
    else:
        k = f'<div class="kick">{s["kick"]}</div>' if s.get("kick") else ""
        sub = f'<p>{s["sub"]}</p>' if s.get("sub") else ""
        cls = " sm" if len(s["text"]) > 46 else ""
        body = f'{k}<h1 class="{cls.strip()}">{s["text"]}</h1>{sub}'
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>'
            f'<body>{body}<div class="dots">{dots}</div></body>')


def shoot(slides, outdir: Path):
    from playwright.sync_api import sync_playwright
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME,
                              args=["--no-sandbox", "--disable-dev-shm-usage",
                                    "--font-render-hinting=none"])
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for i, s in enumerate(slides):
            pg.set_content(slide_html(s, i, len(slides)))
            pg.wait_for_timeout(60)
            f = outdir / f"slide-{i:02d}.png"
            pg.screenshot(path=str(f))
            paths.append(f)
        b.close()
    return paths


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slides", type=Path, help="JSON list of slide specs")
    ap.add_argument("--audio", type=Path)
    ap.add_argument("--timings", type=Path,
                    help="timing map from generate_audio.py --timings; each "
                         "slide's 'seg' names the last line it covers")
    ap.add_argument("--out", type=Path, default=ROOT / "video" / "intro.mp4")
    ap.add_argument("--frames", action="store_true", help="stills only")
    ap.add_argument("--poster", type=Path,
                    help="also write a poster JPEG. Generated here rather "
                         "than by hand so it cannot go stale when the deck "
                         "changes — one shipped showing a slide that had "
                         "since been edited.")
    ap.add_argument("--poster-slide", type=int, default=1,
                    help="slide the poster comes from (default 1: the "
                         "formula, the most specific still)")
    a = ap.parse_args()

    slides = json.loads(a.slides.read_text())
    if a.timings:
        # Cut on the narration: a slide runs until its last line finishes.
        tm = json.loads(a.timings.read_text())
        segs, total, prev = tm["segments"], tm["duration"], 0.0
        for sl in slides:
            end = segs[sl["seg"]]["end"] if sl["seg"] < len(segs) else total
            sl["secs"] = round(max(0.6, end - prev), 3)
            prev = end
        slides[-1]["secs"] = round(slides[-1]["secs"] + max(0.0, total - prev), 3)
        print("slide durations: " + ", ".join(f"{s['secs']:.1f}s" for s in slides))
    frames_dir = ROOT / "build" / "frames"
    paths = shoot(slides, frames_dir)
    print(f"rendered {len(paths)} slides -> {frames_dir}")
    if a.frames:
        return 0

    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as t:
        for s, f in zip(slides, paths):
            t.write(f"file '{f}'\nduration {s['secs']}\n")
        t.write(f"file '{paths[-1]}'\n")       # concat demuxer needs the last twice
        lst = t.name
    a.out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst]
    if a.audio:
        cmd += ["-i", str(a.audio)]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
            "-preset", "slow", "-crf", "23",
            "-vf", "scale=%d:%d,format=yuv420p" % (W, H),
            "-movflags", "+faststart"]
    if a.audio:
        cmd += ["-c:a", "aac", "-b:a", "128k", "-shortest"]
    cmd += [str(a.out)]
    subprocess.run(cmd, check=True)
    print(f"wrote {a.out} — {a.out.stat().st_size/1_048_576:.1f} MB")

    if a.poster:
        i = max(0, min(a.poster_slide, len(slides) - 1))
        at = sum(x.get("secs", 0) for x in slides[:i]) + slides[i].get("secs", 2) / 2
        subprocess.run([ff, "-y", "-ss", f"{at:.2f}", "-i", str(a.out),
                        "-vframes", "1", "-q:v", "3", str(a.poster)],
                       check=True, capture_output=True)
        print(f"  poster {a.poster.name} — slide {i} at {at:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
