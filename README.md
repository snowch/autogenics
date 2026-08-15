# autogenics

Scripts and guided-audio recordings for **autogenic training** — Schultz's six
standard exercises.

The written script is the single source of truth. The audio is rendered from it
by `tools/generate_audio.py`, so the recording can never drift from the text:
edit the markdown, re-run the tool.

## Sessions

| Exercise | Script | Recording | Length |
| --- | --- | --- | --- |
| 1 — Heaviness (arms) | [`script/arm-heaviness.md`](script/arm-heaviness.md) | [`audio/arm-heaviness.mp3`](audio/arm-heaviness.mp3) | 15:44 |

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
| `text <!-- safety -->` | narrated normally, but dropped when `--no-safety` is passed |

Everything outside the markers — safety notes, practice guidance, production
notes — is for the reader and is ignored by the renderer.

## Rendering the audio

```bash
pip install requests imageio-ffmpeg

export ELEVENLABS_API_KEY=sk_...          # never commit this
python3 tools/generate_audio.py script/arm-heaviness.md \
    -o audio/arm-heaviness.mp3
```

Useful flags: `--voice-id`, `--model-id`, `--speed`, `--stretch`,
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

This path needs no API access at all. It is a usable fallback, but at 16 kHz
it sounds noticeably duller than the ElevenLabs render.

## Exporting the narration text

To audition voices in the ElevenLabs UI, or to hand the words to a human
narrator, export the narration on its own:

```bash
# narration only — safe to paste into a TTS UI
python3 tools/generate_audio.py script/arm-heaviness.md --no-safety \
    --prompt-style speech-only \
    --export-prompt prompts/arm-heaviness.11labs.speech-only.txt

# same text with [pause Ns] cues kept, for review
python3 tools/generate_audio.py script/arm-heaviness.md --no-safety \
    --export-prompt prompts/arm-heaviness.11labs.txt
```

Checked in under [`prompts/`](prompts/):

| File | Style | Use |
| --- | --- | --- |
| `arm-heaviness.11labs.speech-only.txt` | narration only | safe to paste into the ElevenLabs UI |
| `arm-heaviness.11labs.txt` | `[pause Ns]` cues kept | reading and review **only** |
| `arm-heaviness.11labs.breaks.txt` | `<break/>` tags | UI pastes where some pause is better than none |

**The `[pause Ns]` cues are annotations, not instructions.** ElevenLabs has no
idea what they mean and will read them aloud as words. Only ever paste the
speech-only or breaks file into a TTS UI.

### Why the UI cannot reproduce this session

ElevenLabs caps a single `<break/>` at **3 seconds**, and chaining many in a row
makes the voice drift or glitch. This script rests for 8–25 seconds between
formulas, so 57 of its 58 pauses need chaining — up to nine tags in a row. The
`breaks` file is generated for completeness and warns you when it exports, but
the result is approximate at best.

`generate_audio.py` sidesteps the limit entirely: it asks ElevenLabs only for
speech, one segment at a time, and lays down the silence itself as digital
samples. That is the only route to the exact timings, and the pauses *are* the
exercise.

## Output

Mono MP3 at the engine's native sample rate, loudness-normalised to −19 LUFS
with −2 dBTP of headroom, which suits quiet listening in a dark room. Pass
`--no-normalize` to skip.

The committed recording was rendered with ElevenLabs (Charlotte,
`eleven_multilingual_v2`) at 24 kHz mono, 15:44 — 5.2 minutes of speech around
10.5 minutes of silence. Built with `--no-safety`, so the cancellation
rationale is in the script but not the audio; drop that flag to include it.

## Pacing

Guided relaxation runs at roughly **80–110 words per minute**; conversational
speech is about 150. Hitting that takes three settings working together, since
none is sufficient alone:

| Lever | Effect |
| --- | --- |
| `--speed 0.7` | ElevenLabs' slowest; on its own this script still ran at 129 wpm |
| sentence-level segments in the script | most of the slowness in real relaxation audio lives in the gaps *between* phrases, not in stretched phonemes |
| `--stretch 0.85` | per-segment `atempo`, pitch-preserving, closes the remaining gap |

Measured on the committed render: **110 wpm**, 2.0:1 silence to speech.
Stretch is applied to each segment *after* the cache and never to the assembled
timeline, so scripted pause lengths stay exact and re-tuning it costs no API
calls. Pass `--stretch 1.0` to disable.
