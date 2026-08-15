#!/usr/bin/env bash
# Download a Piper voice for the offline TTS path.
#
#   ./tools/fetch_piper_voice.sh                     # en-us-lessac-medium
#   ./tools/fetch_piper_voice.sh voice-en-gb-southern_english_female-low
#
# Voices land in ./voices/ and are gitignored.
set -euo pipefail

VOICE="${1:-voice-en-us-lessac-medium}"
BASE="https://github.com/rhasspy/piper/releases/download/v0.0.2"
DEST="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/voices"

mkdir -p "$DEST"
echo "Fetching $VOICE …"
curl -sSL --retry 4 --retry-delay 2 "$BASE/$VOICE.tar.gz" \
  | tar xz -C "$DEST"

echo "Installed into $DEST:"
ls -1 "$DEST"/*.onnx
