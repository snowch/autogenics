#!/usr/bin/env bash
# Regenerate every prompt file in prompts/ from the scripts.
# Run this after editing any script, so the exports cannot drift from it.
#
#   ./tools/export_prompts.sh            # rewrite
#   ./tools/export_prompts.sh --check    # fail if out of date (for CI)
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

CHECK=0
[ "${1:-}" = "--check" ] && CHECK=1
GEN="python3 tools/generate_audio.py"
status=0

for script in script/*.md; do
  base="prompts/$(basename "${script%.md}").11labs"
  for style in speech-only markers breaks; do
    case $style in
      speech-only) out="$base.speech-only.txt" ;;
      markers)     out="$base.txt" ;;
      breaks)      out="$base.breaks.txt" ;;
    esac
    tmp=$(mktemp)
    $GEN "$script" --no-safety --prompt-style "$style" --export-prompt "$tmp" >/dev/null
    if [ "$CHECK" = 1 ]; then
      if ! diff -q "$tmp" "$out" >/dev/null 2>&1; then
        echo "STALE: $out"; status=1
      fi
      rm -f "$tmp"
    else
      mkdir -p "$(dirname "$out")"; mv "$tmp" "$out"; echo "wrote $out"
    fi
  done
done

[ "$CHECK" = 1 ] && [ "$status" = 0 ] && echo "all prompt exports up to date"
exit $status
