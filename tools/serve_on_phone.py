#!/usr/bin/env python3
"""Serve the app from an Android phone, so it can be installed properly.

Run this in Pydroid 3 (or Termux). It finds heaviness-pwa.zip in your
Downloads, unpacks it, and serves it at http://localhost:8000.

Then, in Chrome:  http://localhost:8000  ->  menu  ->  Install app

You only need this once. Installing runs the service worker, which caches the
whole app on the device, so afterwards it works with this script closed and
the phone offline.

Works anywhere Python does — the same script serves the folder on a laptop.
"""
import http.server, os, socket, socketserver, sys, zipfile
from pathlib import Path

PORT = 8000
ZIP = "heaviness-pwa.zip"

HERE = Path(__file__).resolve().parent if "__file__" in dir() else Path.cwd()
LOOK = [HERE, Path.cwd(),
        Path("/storage/emulated/0/Download"), Path("/sdcard/Download"),
        Path("/storage/emulated/0/Documents"), Path("/storage/emulated/0"),
        Path.home() / "Download", Path.home() / "Downloads", Path.home()]

DENIED = """
Android blocked access to that file.

Pydroid can see your Downloads folder but not read from it until you grant
full file access. Do this:

    Settings -> Apps -> Pydroid 3 -> Permissions
      -> Files and media -> Allow management of all files

Then run this again.

If that option isn't there, move both {zip} and this script into Pydroid's own
folder instead, using Pydroid's built-in file browser, and run it from there.
"""


def exists(p: Path) -> bool:
    """Path.exists() itself raises when a parent directory is unreadable,
    which is exactly what Android's scoped storage does."""
    try:
        return p.exists()
    except OSError:
        return False


def readable(p: Path) -> bool:
    try:
        with open(p, "rb") as f:
            f.read(1)
        return True
    except (PermissionError, OSError):
        return False


def writable_dir(candidates) -> Path:
    import tempfile
    for d in candidates:
        try:
            d.mkdir(parents=True, exist_ok=True)
            t = d / ".write-test"
            t.write_text("x"); t.unlink()
            return d
        except (PermissionError, OSError):
            continue
    return Path(tempfile.mkdtemp(prefix="heaviness-"))


def find_site() -> Path:
    """Return a directory containing index.html, unpacking the zip if needed."""
    for d in LOOK:
        for cand in (d / "heaviness", d):
            if exists(cand / "index.html") and readable(cand / "index.html"):
                return cand

    for d in LOOK:
        z = d / ZIP
        if not exists(z):
            continue
        if not readable(z):
            sys.exit(DENIED.format(zip=ZIP))
        dest = writable_dir([z.parent / "heaviness", HERE / "heaviness",
                             Path.home() / "heaviness"])
        print(f"Unpacking {z.name}\n        -> {dest}")
        try:
            with zipfile.ZipFile(z) as f:
                f.extractall(dest)
        except PermissionError:
            sys.exit(DENIED.format(zip=ZIP))
        return dest

    sys.exit(
        f"Couldn't find {ZIP} or an unpacked copy.\n\n"
        "Put the zip in your Downloads folder — or next to this script — and\n"
        "run it again. Looked in:\n  " + "\n  ".join(str(d) for d in LOOK))


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".webmanifest": "application/manifest+json",
                      ".mp3": "audio/mpeg", ".js": "text/javascript"}

    def end_headers(self):
        # A stale service worker would pin the phone to an old build.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *a):
        pass


def lan_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1)); ip = s.getsockname()[0]; s.close()
        return ip
    except Exception:
        return ""


def main() -> int:
    site = find_site()
    os.chdir(site)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\nServing {site}\n")
        print("  On this phone, open Chrome and go to:")
        print(f"      http://localhost:{PORT}")
        print("  Then: menu (⋮) -> Install app\n")
        ip = lan_ip()
        if ip:
            print(f"  From another device on the same wifi: http://{ip}:{PORT}")
            print("  (that address can't install — only localhost counts as secure)\n")
        print("  Once it says installed, you can stop this and close Pydroid.")
        print("  The app keeps working offline.\n")
        print("Ctrl-C, or the stop button in Pydroid, to quit.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
