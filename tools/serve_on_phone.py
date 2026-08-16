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
LOOK = ["/storage/emulated/0/Download", "/sdcard/Download",
        "/storage/emulated/0/Documents", os.path.expanduser("~/Download"),
        os.path.expanduser("~/Downloads"), os.getcwd()]


def find_site() -> Path:
    """Return a directory containing index.html, unpacking the zip if needed."""
    for d in LOOK:
        p = Path(d)
        if (p / "heaviness" / "index.html").exists():
            return p / "heaviness"
        if (p / "index.html").exists() and (p / "manifest.webmanifest").exists():
            return p
    for d in LOOK:
        z = Path(d) / ZIP
        if z.exists():
            dest = z.parent / "heaviness"
            print(f"Unpacking {z.name} -> {dest}")
            with zipfile.ZipFile(z) as f:
                f.extractall(dest)
            return dest
    sys.exit(
        f"Couldn't find {ZIP} or an unpacked copy.\n"
        "Put the zip in your Downloads folder and run this again.\n"
        "Looked in:\n  " + "\n  ".join(LOOK))


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
