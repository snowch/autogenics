#!/usr/bin/env python3
"""Derive a standalone, self-contained build of app/index.html.

The app plays audio from ../audio/ when served from the repo. A published or
sideloaded copy has no such neighbours and, for artifacts, a CSP that blocks
every external host — so this inlines the recordings as data: URIs and strips
the document skeleton the artifact host supplies itself.

    python3 tools/build_app_artifact.py            # -> build/autogenics.html
    python3 tools/build_app_artifact.py --standalone   # keep <html> wrapper
"""
import base64, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
# One source for the asset map. This file used to keep its own copy, which is
# how the artifact and the PWA drift apart without anything failing.
from build_pwa import TRACKS  # noqa: E402
BITRATE = "32k"          # speech-only; keeps the whole page well inside 16 MB
VIDEO_W, VIDEO_CRF = 540, 30   # films are static slides; text stays crisp


def ffmpeg() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def encode(src: Path) -> str:
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as t:
        out = Path(t.name)
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", str(src),
                    "-codec:a", "libmp3lame", "-b:a", BITRATE, "-ac", "1",
                    str(out)], check=True)
    data = base64.b64encode(out.read_bytes()).decode()
    kb = out.stat().st_size / 1024
    out.unlink()
    print(f"  {src.name:34s} {src.stat().st_size/1024:7.0f} KB -> {kb:6.0f} KB")
    return "data:audio/mpeg;base64," + data


def shrink(src: Path) -> bytes:
    """Re-encode a film small enough to inline.

    The films are static typographic slides, so they survive a halving of
    resolution with the text still crisp — checked by eye, not assumed. Seven
    of them at full size pushed this file past 17 MB, which is a poor thing to
    open on a phone. The PWA still serves the full-quality originals; this
    copy exists only because everything here has to fit in one file.
    """
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as t:
        out = Path(t.name)
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", str(src),
                    "-vf", f"scale={VIDEO_W}:-2", "-c:v", "libx264",
                    "-crf", str(VIDEO_CRF), "-preset", "slow",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "48k",
                    "-movflags", "+faststart", str(out)], check=True)
    data = out.read_bytes()
    print(f"  {src.name:34s} {src.stat().st_size/1024:7.0f} KB -> {len(data)/1024:6.0f} KB")
    out.unlink()
    return data


def main() -> int:
    standalone = "--standalone" in sys.argv
    html = (ROOT / "app" / "index.html").read_text(encoding="utf-8")

    print("Inlining audio:")
    blob = ",\n  ".join(
        f'{k}:"{encode(ROOT / "audio" / v)}"' for k, v in TRACKS.items())

    from build_pwa import build_id
    html = html.replace('<script>\n"use strict";',
                        f'<script>\n"use strict";\nwindow.__BUILD__="{build_id()}";', 1)
    html = html.replace("<script>\n\"use strict\";",
                        "<script>\n\"use strict\";\nwindow.__AUDIO__={\n  "
                        + blob + "\n};", 1)

    if not standalone:
        # The artifact host wraps content in its own <!doctype>/<head>/<body>.
        head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
        body = re.search(r"<body>(.*?)</body>", html, re.S).group(1)
        keep = "".join(re.findall(r"<title>.*?</title>|<style>.*?</style>",
                                  head, re.S))
        html = keep + body

    dest = ROOT / "build" / "autogenics.html"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print(f"\nWrote {dest} — {dest.stat().st_size/1_048_576:.1f} MB"
          f"{' (standalone)' if standalone else ' (artifact-shaped)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
