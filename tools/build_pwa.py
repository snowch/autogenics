#!/usr/bin/env python3
"""Build an installable PWA into docs/ from app/index.html.

Produces a self-contained static site: the app, compressed audio, a web app
manifest, icons, and a service worker that precaches everything so practice
works with no signal. Serve docs/ from any static host — GitHub Pages reads it
directly — then "Add to Home Screen" on iOS or "Install app" on Android.

    python3 tools/build_pwa.py
"""
import json, re, shutil, struct, subprocess, sys, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TRACKS = {"explainer": "explainer.mp3", "s1": "arm-heaviness-example.mp3",
          "s2": "arm-heaviness-example-2.mp3", "s3": "arm-heaviness-example-3.mp3",
          "warmth": "at-warmth.mp3", "heartbeat": "at-heartbeat.mp3",
          "breathing": "at-breathing.mp3", "solar": "at-solar-plexus.mp3",
          "forehead": "at-forehead.mp3"}
BITRATE = "32k"
BG, FG = (0x0D, 0x12, 0x18), (0xE0, 0xA1, 0x5C)


def ffmpeg() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def png(size: int, path: Path, pad: float = 0.0) -> None:
    """A filled circle on the app's ground — written without an image library."""
    c, r = size / 2, size * (0.5 - pad) * 0.62
    rows = bytearray()
    for y in range(size):
        rows.append(0)                                   # filter: none
        for x in range(size):
            d = ((x + .5 - c) ** 2 + (y + .5 - c) ** 2) ** .5
            # antialias the edge over one pixel
            a = max(0.0, min(1.0, r - d + .5))
            rows += bytes(round(BG[i] + (FG[i] - BG[i]) * a) for i in range(3))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
        + chunk(b"IEND", b""))


def main() -> int:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    (DOCS / "audio").mkdir(parents=True)

    print("Audio:")
    for name in TRACKS.values():
        out = DOCS / "audio" / name
        subprocess.run([ffmpeg(), "-y", "-loglevel", "error",
                        "-i", str(ROOT / "audio" / name), "-codec:a", "libmp3lame",
                        "-b:a", BITRATE, "-ac", "1", str(out)], check=True)
        print(f"  {name:30s} {out.stat().st_size/1024:6.0f} KB")

    print("Icons:")
    for size, name in ((192, "icon-192.png"), (512, "icon-512.png")):
        png(size, DOCS / name); print(f"  {name}")
    png(180, DOCS / "apple-touch-icon.png", pad=.06); print("  apple-touch-icon.png")

    html = (ROOT / "app" / "index.html").read_text(encoding="utf-8")
    html = html.replace("'../audio/", "'./audio/")
    (DOCS / "video").mkdir(exist_ok=True)
    shutil.copy(ROOT / "video" / "intro.mp4", DOCS / "video" / "intro.mp4")
    html = html.replace("'../video/", "'./video/")
    print(f"  intro.mp4 {(DOCS/'video'/'intro.mp4').stat().st_size/1024:6.0f} KB")
    head = ("""<link rel="manifest" href="./manifest.webmanifest">
<link rel="apple-touch-icon" href="./apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Heaviness">
<meta name="description" content="Autogenic training: the six standard exercises, at the dose the method actually calls for.">
</head>""")
    html = html.replace("</head>", head, 1)
    html = html.replace("</body>", """<script>
if('serviceWorker' in navigator){
  window.addEventListener('load',()=>navigator.serviceWorker
    .register('./sw.js').catch(()=>{}));
}
</script>
</body>""", 1)
    (DOCS / "index.html").write_text(html, encoding="utf-8")

    (DOCS / "manifest.webmanifest").write_text(json.dumps({
        "name": "Heaviness — autogenic training",
        "short_name": "Heaviness",
        "description": "The six standard exercises, at the dose the method actually calls for.",
        "start_url": "./", "scope": "./",
        "display": "standalone", "orientation": "portrait",
        "background_color": "#0D1218", "theme_color": "#0D1218",
        "icons": [{"src": "./icon-192.png", "sizes": "192x192", "type": "image/png",
                   "purpose": "any maskable"},
                  {"src": "./icon-512.png", "sizes": "512x512", "type": "image/png",
                   "purpose": "any maskable"}],
    }, indent=2), encoding="utf-8")

    assets = ["./", "./index.html", "./manifest.webmanifest", "./video/intro.mp4",
              "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png"] + \
             [f"./audio/{n}" for n in TRACKS.values()]
    # Cache name carries the audio byte-count, so a re-render invalidates it.
    ver = sum((DOCS / "audio" / n).stat().st_size for n in TRACKS.values()) \
        + (DOCS / "video" / "intro.mp4").stat().st_size
    (DOCS / "sw.js").write_text(f"""const CACHE='heaviness-{ver}';
const ASSETS={json.dumps(assets)};
self.addEventListener('install',e=>{{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));
}});
self.addEventListener('activate',e=>{{
  e.waitUntil(caches.keys()
    .then(k=>Promise.all(k.filter(n=>n!==CACHE).map(n=>caches.delete(n))))
    .then(()=>self.clients.claim()));
}});
/* Cache first: once installed the app must work with no signal at all. */
self.addEventListener('fetch',e=>{{
  if(e.request.method!=='GET')return;
  e.respondWith(caches.match(e.request,{{ignoreSearch:true}})
    .then(r=>r||fetch(e.request).then(res=>{{
      const copy=res.clone();
      caches.open(CACHE).then(c=>c.put(e.request,copy)).catch(()=>{{}});
      return res;
    }}).catch(()=>caches.match('./index.html'))));
}});
""", encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    total = sum(f.stat().st_size for f in DOCS.rglob("*") if f.is_file())
    print(f"\nWrote {DOCS} — {total/1_048_576:.1f} MB, "
          f"{len(list(DOCS.rglob('*')))} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
