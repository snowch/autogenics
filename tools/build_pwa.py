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
# key in the app's AUDIO map -> file. Adding a film means adding one row here.
FILMS = [("afterFirst", "after-first.mp4", "after-first-poster.jpg"),
         ("bWarmth", "brief-warmth.mp4", "brief-warmth-poster.jpg"),
         ("bHeartbeat", "brief-heartbeat.mp4", "brief-heartbeat-poster.jpg"),
         ("bBreathing", "brief-breathing.mp4", "brief-breathing-poster.jpg"),
         ("bSolar", "brief-solar.mp4", "brief-solar-poster.jpg"),
         ("bForehead", "brief-forehead.mp4", "brief-forehead-poster.jpg"),
         ("finished", "finished.mp4", "finished-poster.jpg")]

TRACKS = {"s1": "arm-heaviness-example.mp3",
          "all": "at-heaviness-all.mp3",
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


def asset_version() -> str:
    """The number the service worker caches under.

    build_id() names the commit at build time, which is the commit *before* the
    one the build ships in — accurate about the tree, misleading about the
    deploy. This is derived from the bytes actually written, so two devices
    showing the same number are running the same files, whatever git thinks.
    """
    tot = 0
    for n in TRACKS.values():
        f = DOCS / "audio" / n
        if f.exists(): tot += f.stat().st_size
    for _, mp4, _ in FILMS:
        f = DOCS / "video" / mp4
        if f.exists(): tot += f.stat().st_size
    return str(tot)


def build_id() -> str:
    """Short commit for the stamp shown under Your record.

    A deploy that failed and a worker that never updated are indistinguishable
    from the device, which is precisely the confusion this answers.
    """
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                               capture_output=True, text=True).stdout.strip()
        return sha + ("+" if dirty else "")
    except Exception:
        return "unknown"


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
    html = html.replace("<script>\n\"use strict\";",
                        f'<script>\n"use strict";\n'
                        f'window.__BUILD__="{build_id()}";'
                        'window.__ASSETS__="@@ASSETS@@";', 1)
    (DOCS / "video").mkdir(exist_ok=True)
    for _, mp4, poster in FILMS:
        for n in (mp4, poster):
            src = ROOT / "video" / n
            if not src.exists():
                raise SystemExit(f"video/{n} missing — rebuild it before publishing")
            shutil.copy(src, DOCS / "video" / n)
        print(f"  {mp4:24s} {(DOCS/'video'/mp4).stat().st_size/1024:6.0f} KB")
    html = html.replace("'../video/", "'./video/")
    head = ("""<link rel="manifest" href="./manifest.webmanifest">
<link rel="icon" href="./icon-192.png">
<link rel="apple-touch-icon" href="./apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Switch">
<meta name="description" content="Autogenic training: the six standard exercises, at the dose the method actually calls for.">
</head>""")
    html = html.replace("</head>", head, 1)
    # Registering and walking away is not enough. The worker skipWaiting()s and
    # claims clients, so a deploy activates — but the page already on screen
    # keeps rendering the HTML it loaded, and an installed PWA is rarely
    # navigated away from, so the user sits on a stale build until they think
    # to clear site data. Check on launch and on resume, and reload once when a
    # new worker takes over.
    html = html.replace("</body>", """<script>
(function(){
if('serviceWorker' in navigator){
  /* claimed is a running flag, not a snapshot. Read once at load it is false
     on a first-ever visit, stays false when that first worker claims the page,
     and then swallows the reload for the genuine update that follows. */
  var claimed = !!navigator.serviceWorker.controller, pending = false, waitTimer = null;
  /* Never reload out from under a running practice. Someone is lying down with
     their eyes shut for ninety seconds; restarting the app mid-exercise is the
     one moment this must not happen. The same goes for a film playing and for
     the rating screen, which holds a result not yet written down. */
  function busy(){
    return !!document.querySelector('#practice.on, #brief.on, #rating.on');
  }
  function swap(){
    if(window.__reloading) return;
    if(busy()){                       /* wait, and keep waiting */
      pending = true;
      if(!waitTimer) waitTimer = setInterval(function(){
        if(!busy()){ clearInterval(waitTimer); waitTimer = null; swap(); }
      }, 4000);
      return;
    }
    window.__reloading = true;
    location.reload();
  }
  navigator.serviceWorker.addEventListener('controllerchange', function(){
    if(!claimed){ claimed = true; return; }   /* first install: nothing to replace */
    swap();
  });
  var check = function(){
    navigator.serviceWorker.getRegistration()
      .then(function(r){ if(r) r.update(); }).catch(function(){});
  };
  window.addEventListener('load', function(){
    navigator.serviceWorker.register('./sw.js').then(check).catch(function(){});
  });
  document.addEventListener('visibilitychange', function(){
    if(document.hidden) return;
    if(pending) return swap();      /* an update has been waiting for a gap */
    check();
  });
}
})();
</script>
</body>""", 1)
    html = html.replace("@@ASSETS@@", asset_version())
    (DOCS / "index.html").write_text(html, encoding="utf-8")

    (DOCS / "manifest.webmanifest").write_text(json.dumps({
        "name": "Switch",
        "short_name": "Switch",
        "description": "A trained response, in ninety seconds a day.",
        "start_url": "./", "scope": "./",
        "display": "standalone", "orientation": "portrait",
        "background_color": "#0D1218", "theme_color": "#0D1218",
        "icons": [{"src": "./icon-192.png", "sizes": "192x192", "type": "image/png",
                   "purpose": "any maskable"},
                  {"src": "./icon-512.png", "sizes": "512x512", "type": "image/png",
                   "purpose": "any maskable"}],
    }, indent=2), encoding="utf-8")

    films = [f"./video/{n}" for _, mp4, poster in FILMS for n in (mp4, poster)]
    assets = ["./", "./index.html", "./manifest.webmanifest",
              "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png"] + films + \
             [f"./audio/{n}" for n in TRACKS.values()]
    # Cache name carries every asset's byte-count, so a re-render invalidates it.
    ver = sum((DOCS / "audio" / n).stat().st_size for n in TRACKS.values()) \
        + sum((DOCS / "video" / mp4).stat().st_size for _, mp4, _ in FILMS)
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
