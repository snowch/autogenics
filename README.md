# autogenics

Scripts and guided-audio recordings for **autogenic training** — Schultz's six
standard exercises.

The written script is the single source of truth. The audio is rendered from it
by `tools/generate_audio.py`, so the recording can never drift from the text:
edit the markdown, re-run the tool.

## Sessions

| Exercise | Script | Recording | Length |
| --- | --- | --- | --- |
| 1 — Heaviness (arms) | [`script/arm-heaviness.md`](script/arm-heaviness.md) | [`audio/arm-heaviness.mp3`](audio/arm-heaviness.mp3) | 12:24 |

> **Safety.** Do not listen while driving. Autogenic training lowers blood
> pressure and heart rate — check with a clinician first if you have low blood
> pressure, a heart condition, diabetes, epilepsy, or are in treatment for a
> psychotic disorder. Every session ends with a **cancellation** ("take-back");
> it is part of the exercise, so do not stop the recording early.

## Script format

Everything between `<!-- narration:start -->` and `<!-- narration:end -->` is
spoken. Within that region:

| Line | Meaning |
| --- | --- |
| ordinary text | narrated; consecutive lines join into one paragraph, blank lines separate segments |
| `[pause 12]` | 12 seconds of silence |
| `# heading` | structure only, never spoken |
| `> note` | delivery note for the voice, never spoken |

Everything outside the markers — safety notes, practice guidance, production
notes — is for the reader and is ignored by the renderer.

## Rendering the audio

```bash
pip install requests imageio-ffmpeg

export ELEVENLABS_API_KEY=sk_...          # never commit this
python3 tools/generate_audio.py script/arm-heaviness.md \
    -o audio/arm-heaviness.mp3
```

Useful flags: `--voice-id`, `--model-id`, `--speed` (`<1` is slower),
`--stability`, `--lufs`, `--dry-run`. Segments are cached under `.cache/tts/`
and keyed by voice, settings and text, so re-running after a small script edit
only re-synthesises what changed.

### Offline fallback

If the ElevenLabs API is unreachable, [Piper](https://github.com/rhasspy/piper)
runs entirely locally:

```bash
pip install piper-tts
./tools/fetch_piper_voice.sh                 # ~58 MB into voices/

python3 tools/generate_audio.py script/arm-heaviness.md \
    --engine piper --piper-model voices/en-us-lessac-medium.onnx \
    --bitrate 64k -o audio/arm-heaviness.mp3
```

The committed recording was produced this way (en-us-lessac-medium, 16 kHz
mono). It is clear and usable, but ElevenLabs gives a warmer, higher-fidelity
result — re-render with the default engine when you have API access.

## Output

Mono MP3, loudness-normalised to −19 LUFS with −2 dBTP of headroom, which suits
quiet listening in a dark room. Pass `--no-normalize` to skip.
