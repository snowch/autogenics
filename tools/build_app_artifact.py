#!/usr/bin/env python3
"""Derive a standalone, self-contained build of app/index.html.

The app plays audio from ../audio/ when served from the repo. A published or
sideloaded copy has no such neighbours and, for artifacts, a CSP that blocks
every external host — so this inlines the recordings as data: URIs and strips
the document skeleton the artifact host supplies itself.

    python3 tools/build_app_artifact.py            # -> build/heaviness.html
    python3 tools/build_app_artifact.py --standalone   # keep <html> wrapper
"""
import base64, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKS = {"explainer": "explainer.mp3",
          "s1": "arm-heaviness-example.mp3",
          "s2": "arm-heaviness-example-2.mp3",
          "s3": "arm-heaviness-example-3.mp3",
          "warmth": "at-warmth.mp3",
          "heartbeat": "at-heartbeat.mp3",
          "breathing": "at-breathing.mp3",
          "solar": "at-solar-plexus.mp3",
          "forehead": "at-forehead.mp3"}
BITRATE = "32k"          # speech-only; keeps the whole page well inside 16 MB


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


def main() -> int:
    standalone = "--standalone" in sys.argv
    html = (ROOT / "app" / "index.html").read_text(encoding="utf-8")

    print("Inlining video:")
    vid = ROOT / "video" / "intro.mp4"
    vid_uri = ""
    if vid.exists():
        vid_uri = "data:video/mp4;base64," + base64.b64encode(vid.read_bytes()).decode()
        print(f"  {vid.name:34s} {vid.stat().st_size/1024:7.0f} KB")

    print("Inlining audio:")
    blob = ",\n  ".join(
        f'{k}:"{encode(ROOT / "audio" / v)}"' for k, v in TRACKS.items())
    if vid_uri:
        blob += f',\n  intro:"{vid_uri}"'
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

    dest = ROOT / "build" / "heaviness.html"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print(f"\nWrote {dest} — {dest.stat().st_size/1_048_576:.1f} MB"
          f"{' (standalone)' if standalone else ' (artifact-shaped)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
