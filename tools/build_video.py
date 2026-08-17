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
  padding:110px 96px;overflow:hidden;position:relative}
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
.mark{position:absolute;left:96px;bottom:74px;font-family:'DejaVu Sans Mono',monospace;
  font-size:22px;letter-spacing:.2em;text-transform:uppercase;color:#3A4653}
.dots{position:absolute;right:96px;bottom:74px;display:flex;gap:9px}
.dots i{width:9px;height:9px;border-radius:50%%;background:#243140;display:block}
.dots i.on{background:#E0A15C;width:30px;border-radius:5px}
""" % (W, H)


def slide_html(s, idx, total):
    dots = "".join(f'<i class="{"on" if i==idx else ""}"></i>' for i in range(total))
    kind = s.get("kind", "point")
    if kind == "formula":
        body = f'<div class="rule"></div><div class="formula">{s["text"]}</div>'
    elif kind == "stats":
        cells = "".join(f'<div><div class="n">{n}</div><div class="c">{c}</div></div>'
                        for n, c in s["stats"])
        body = (f'<div class="kick">{s.get("kick","")}</div>'
                f'<h1 class="sm">{s["text"]}</h1><div class="stats">{cells}</div>')
    else:
        k = f'<div class="kick">{s["kick"]}</div>' if s.get("kick") else ""
        sub = f'<p>{s["sub"]}</p>' if s.get("sub") else ""
        cls = " sm" if len(s["text"]) > 46 else ""
        body = f'{k}<h1 class="{cls.strip()}">{s["text"]}</h1>{sub}'
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>'
            f'<body>{body}<div class="mark">Autogenic training</div>'
            f'<div class="dots">{dots}</div></body>')


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
    ap.add_argument("--out", type=Path, default=ROOT / "video" / "intro.mp4")
    ap.add_argument("--frames", action="store_true", help="stills only")
    a = ap.parse_args()

    slides = json.loads(a.slides.read_text())
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
            "-vf", "scale=%d:%d,format=yuv420p" % (W, H)]
    if a.audio:
        cmd += ["-c:a", "aac", "-b:a", "128k", "-shortest"]
    cmd += [str(a.out)]
    subprocess.run(cmd, check=True)
    print(f"wrote {a.out} — {a.out.stat().st_size/1_048_576:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
