# autogenics

Scripts and guided-audio recordings for **autogenic training** — Schultz's six
standard exercises.

The written script is the single source of truth. The audio is rendered from it
by `tools/generate_audio.py`, so the recording can never drift from the text:
edit the markdown, re-run the tool.

## Sessions

| Track | Script | Recording | Length |
| --- | --- | --- | --- |
| Explainer — listen once first | [`script/explainer.md`](script/explainer.md) | [`audio/explainer.mp3`](audio/explainer.mp3) | 6:09 |
| **Stage 1 — right arm** | [`script/arm-heaviness-example.md`](script/arm-heaviness-example.md) | [`audio/arm-heaviness-example.mp3`](audio/arm-heaviness-example.mp3) | 2:32 |
| **Stage 2 — both arms, in turn** | [`script/arm-heaviness-example-2.md`](script/arm-heaviness-example-2.md) | [`audio/arm-heaviness-example-2.mp3`](audio/arm-heaviness-example-2.mp3) | 2:15 |
| **Stage 3 — both arms together** | [`script/arm-heaviness-example-3.md`](script/arm-heaviness-example-3.md) | [`audio/arm-heaviness-example-3.mp3`](audio/arm-heaviness-example-3.mp3) | 2:05 |
| Warmth — step 4 | [`script/at-warmth.md`](script/at-warmth.md) | [`audio/at-warmth.mp3`](audio/at-warmth.mp3) | 1:52 |
| Heartbeat — step 5 | [`script/at-heartbeat.md`](script/at-heartbeat.md) | [`audio/at-heartbeat.mp3`](audio/at-heartbeat.mp3) | 1:56 |
| Breathing — step 6 | [`script/at-breathing.md`](script/at-breathing.md) | [`audio/at-breathing.mp3`](audio/at-breathing.mp3) | 1:52 |
| Warm centre — step 7 | [`script/at-solar-plexus.md`](script/at-solar-plexus.md) | [`audio/at-solar-plexus.mp3`](audio/at-solar-plexus.mp3) | 2:02 |
| Cool head — step 8 | [`script/at-forehead.md`](script/at-forehead.md) | [`audio/at-forehead.mp3`](audio/at-forehead.mp3) | 1:59 |
| Long form, short | [`script/arm-heaviness-short.md`](script/arm-heaviness-short.md) | [`audio/arm-heaviness-short.mp3`](audio/arm-heaviness-short.mp3) | 7:04 |
| Long form, full | [`script/arm-heaviness.md`](script/arm-heaviness.md) | [`audio/arm-heaviness.mp3`](audio/arm-heaviness.mp3) | 14:25 |

## Video slides

`tools/build_video.py` renders narrated video from a list of slide specs: the
slides are HTML, screenshotted with the pre-installed Chromium, then assembled
against a script's own audio. Because the audio pipeline already knows each
segment's duration, cuts land on the narration rather than near it.

```bash
python3 tools/build_video.py slides.json --frames     # stills, for review
python3 tools/build_video.py slides.json --audio audio/intro.mp3
```

1080×1350, the app's palette, and Bitstream Charter — a real book serif that
happens to be installed, rather than a fallback. Three slide kinds so far:
statement, formula, and stats.

The first one is built: [`video/intro.mp4`](video/intro.mp4), 60 seconds, nine
slides, from [`script/intro.md`](script/intro.md).

```bash
python3 tools/generate_audio.py script/intro.md -o audio/intro.mp3 \
    --timings build/intro-timings.json
python3 tools/build_video.py build/intro-slides.json \
    --timings build/intro-timings.json --audio audio/intro.mp3 \
    --out video/intro.mp4
```

`--timings` writes each spoken line's start and end; each slide names the last
line it covers, so cuts land on the narration. Measured drift between audio and
video on the built file: 0.00s.

It replaces the two selling panels of the text onboarding. **The disclaimer and
safety panel stays as text** with an explicit tap to continue — a video can be
skipped, muted, or half-watched, and "they were told in a video" is a weaker
position than "they tapped to acknowledge".

Graphics are diagrammatic, drawn from the app's own vocabulary — the day's three
slots, the step rail, the practice ring — so the video and the product speak the
same visual language. There is no image model in this environment, so
illustration or photography is not available.

## Install it on a phone

`docs/` is a complete, installable PWA — the app, compressed audio, icons, a
manifest, and a service worker that precaches everything so practice works
with no signal. Rebuild it with:

```bash
python3 tools/check_app.py     # syntax-check the JS — run this before publishing
python3 tools/build_pwa.py
```

`check_app.py` parses the inline scripts with `node --check` and verifies that
every `$('#id')` resolves and every audio key is defined. A malformed string
literal takes out the entire script block and leaves a page that renders but
does nothing — grepping the HTML will not catch it, and one shipped that way.

It is committed, so **GitHub Pages can serve it as-is**: repository *Settings →
Pages → Source: Deploy from a branch → this branch, folder `/docs`*. Any static
host works too — the directory has no build step and no backend.

### Without any hosting: serve it from the phone

`tools/serve_on_phone.py` runs in [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3)
or Termux. It finds `heaviness-pwa.zip` in Downloads, unpacks it, and serves it
at `http://localhost:8000`, which Chrome treats as a secure origin — so the
service worker registers and *Install app* appears.

You only need it once. Installing precaches the whole app on the device, so
afterwards it runs with the server stopped and the phone offline.

Note that `file://` is not enough: opening `index.html` from a file manager
gives no service worker, no install, and unreliable `localStorage` — which is
where the practice record lives.

Then, on the phone:

| | |
| --- | --- |
| **iPhone / iPad** | Open the URL **in Safari** (not Chrome), tap Share, then *Add to Home Screen*. It launches full-screen with no browser chrome. |
| **Android** | Open in Chrome, then *Install app* from the ⋮ menu, or *Add to Home screen*. |

After the first load it runs offline. The practice log lives in `localStorage`
on the device.

**What this is not.** A PWA, not an App Store or Play Store build — there is no
review, no store listing, and on iOS no background notifications. Reminders
are the one feature that genuinely needs a native wrapper, and three practices
a day is the mechanism the whole thing depends on. When that matters, the same
`docs/` directory wraps directly with Capacitor for both stores.

## The app

[`app/index.html`](app/index.html) is a single-page app: no build step, no
backend, no network. The record lives in `localStorage`, which keeps
health-adjacent data on the device and leaves a Capacitor or PWA wrapper
straightforward.

```bash
python3 tools/check_app.py                        # syntax-check first
python3 tools/build_app_artifact.py --standalone   # -> build/heaviness.html
```

### The journey is the screen

Three bands, in the order you use them. A **hero card** holds only what you act
on — the phrase, today's three practice slots, one primary button. A **review
card** holds the fourteen-day record and the two conditions for moving on. Then
**the path**: nine steps as a vertical timeline with a status on each, Done,
Now or Later, any of which opens to show what it is.

An earlier version crammed all three into the open step. It carried eight
things at once and read as a wall.

This replaced a Today tab sitting beside a Progress tab. Once progression is
something you can see and tap into, "today" is just the open step — a separate
screen for it duplicated the same state in two places and hid the path. Two
tabs remain: Practice and Learn.

An earlier version drew the six exercises on a small figure, at the place each
is felt. It was removed. It looked considered and told you less than the list
does, which is a fair description of decoration.

### Plain language

User-facing copy avoids terms the reader has no reason to know yet. "Stage"
became "step", "formula" became "phrase", and the take-back is described by
what it does — *finish by waking yourself up* — before it is ever named. The
traditional terms still appear in Learn, glossed on first use, because the
audience for this does eventually meet them in the literature.

### Positioning and claims

Autogenic training is described as a **self-training method** — learning
deliberate access to a state the body normally reaches only on its own — not
as a relaxation practice. That earlier wording was a disclaimer doing double
duty as a description, and it undersold the method: heaviness is one of six
standard exercises, with the meditative exercises and personal formulae beyond
them. The app now maps all six on the Progress screen, marks the two
traditionally taught with an instructor, and is explicit that it covers
heaviness only.

Describing scope is not a health claim. The exposure lives in claims of
outcome, so those are what the copy avoids.

Benefits are described **experientially and never clinically**. The copy says
what the practice feels like and when people reach for it — warmth and weight
in the arms, winding down, settling into sleep, steadying before something that
matters. It names no condition, cites no trial, and promises no outcome.

Nothing in the product asserts a physiological effect. Even the safety
cautions are phrased as cautions rather than claims: *deep relaxation can leave
you light-headed on standing*, not *this lowers your blood pressure*. Every
surface carries "a relaxation practice, not medical treatment or advice".

Keep any future copy on that side of the line. Naming a condition, quoting a
study, or promising a result changes what the product legally is.

The intro closes on a **journey map**, which also lives on Progress as a live
position marker. The six exercises are drawn on a seated figure at the place
each one is felt — heaviness at the arms, warmth at the hands, then chest,
ribs, abdomen, forehead — because the method genuinely runs down the body, and
a map of the body says more than a progress bar. Completed regions fill,
the current one pulses, and each row carries a pip per step plus the day count.

The ladder now runs the full method: eight steps across all six standard
exercises, each adding one phrase to the run-through that precedes it, so a
practice stays around ninety seconds however far along you are. The last step
is the whole sequence with no audio at all.

The heartbeat, warm-centre and cool-head steps carry a caution shown on the
Today screen and again before the first practice of that step, saying which
are traditionally taught in person and who should skip them.

**One principle is wired into it: the app gets quieter as you improve.**
Guided narration is the default for the first three days of a stage; after
that it steps back to a bare timer, and the last rung has no audio at all. An
app equally chatty on day sixty has failed, however good its retention looks.

**The staged examples are what do the work.** It is a single practice at the
dose the method actually calls for — 96 seconds, dominant arm only, six
repetitions — done *with* the listener and then handed over: after the
cancellation it says, in as many words, that they don't need the recording and
should do it themselves three times a day. Play it a handful of times to learn
the shape, not daily.

The longer sessions are for occasional use or for someone who wants the long
form. Frequency is what builds the response; a fourteen-minute session played
once a day is the wrong dose in both directions.

Listen to the explainer once, before the first practice. It carries the
teaching — what passive concentration is, what to expect and when, how often to
practise, and why the cancellation is not optional — so that the sessions never
have to stop and explain themselves. A session that does that breaks the state
it is trying to produce.

The short version is a young-adult cut of the same exercise: identical
formulas, four repetitions per limb instead of six, 5s pauses instead of 8s,
and plainer language. Fewer repetitions is a deliberate departure from Schultz.
The cancellation is **not** shortened in any version.

> **Safety.** Do not listen while driving. Deep relaxation can leave you
> light-headed on standing — check with a clinician first if you have low blood
> pressure, a heart condition, diabetes, epilepsy, or are in treatment for a
> psychotic disorder. These are self-training exercises, not medical treatment or
> advice. Every session ends with a **cancellation** ("take-back");
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
| `[stretch 1.0]` | changes time-stretch for everything after it |

Everything outside the markers — safety notes, practice guidance, production
notes — is for the reader and is ignored by the renderer.

## Rendering the audio

```bash
pip install requests numpy imageio-ffmpeg

export ELEVENLABS_API_KEY=sk_...          # never commit this
python3 tools/generate_audio.py script/arm-heaviness.md \
    -o audio/arm-heaviness.mp3
```

A script can declare its own render settings, which the tool applies before
any CLI flags:

```markdown
<!-- render: --speed 0.9 --stretch 1.0 --lead-in 0.5 -->
```

The explainer uses this. It is the one track that is *not* relaxation audio —
at the session defaults it would come out as a five-minute drone — and keeping
the settings in the file stops a later re-render silently getting it wrong.

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
./tools/export_prompts.sh            # rewrite every file in prompts/
./tools/export_prompts.sh --check    # fail if any is out of date
```

Run it after editing a script. The exports are derived files and will otherwise
drift from their source — they silently had, before `--check` existed. That
mode suits CI.

Three styles are written per script, checked in under [`prompts/`](prompts/):

| Suffix | Style | Use |
| --- | --- | --- |
| `.speech-only.txt` | narration only | safe to paste into the ElevenLabs UI |
| `.txt` | `[pause Ns]` cues kept | reading and review **only** |
| `.breaks.txt` | `<break/>` tags | UI pastes where some pause is better than none |

**The `[pause Ns]` cues are annotations, not instructions.** ElevenLabs has no
idea what they mean and will read them aloud as words. Only ever paste the
speech-only or breaks file into a TTS UI.

### Why the UI cannot reproduce this session

ElevenLabs caps a single `<break/>` at **3 seconds**, and chaining many in a row
makes the voice drift or glitch. These scripts rest for 5–25 seconds between
formulas, so most pauses need chaining — 57 of 84 in the full session, 39 of 45
in the short one, up to nine tags in a row. The `breaks` files are generated
for completeness and warn you on export, but the result is approximate at
best.

`generate_audio.py` sidesteps the limit entirely: it asks ElevenLabs only for
speech, one segment at a time, and lays down the silence itself as digital
samples. That is the only route to the exact timings, and the pauses *are* the
exercise.

## Output

Mono MP3 at the engine's native sample rate, loudness-normalised to −19 LUFS
with −2 dBTP of headroom, which suits quiet listening in a dark room. Pass
`--no-normalize` to skip.

All recordings were rendered with ElevenLabs (Charlotte,
`eleven_multilingual_v2`) at 24 kHz mono. The sessions are built with
`--no-safety`, so the cancellation rationale stays in the script but not the
audio; drop that flag to include it.

## Pacing

Guided relaxation is usually cited at **80–110 words per minute** against about
150 for conversational speech. Two levers control it:

| Lever | Effect |
| --- | --- |
| `--speed 0.7` | ElevenLabs' slowest setting |
| `--stretch 0.85` | per-segment `atempo`, pitch-preserving, applied on top |

Measured on the committed renders: **139 wpm** for the full session, 128 for
the short one, and **163 for the explainer** — which is meant to be brisk, since
it is information rather than induction.

Measure this on *trimmed* speech. Timing whole segments as returned by the API
counts their trailing padding as if it were delivery, which reads about 25 wpm
slower than the voice is actually going. The padding is now trimmed, so the
figure above is the real one.

`[stretch]` mid-script lets one recording hold two paces. Every session uses it
at the cancellation: the take-back is meant to wake the listener, so it runs at
152 wpm against 129 for the induction. Because stretch is applied after the
cache, this costs nothing to add or re-tune.

Sentence-level segmentation in the script does not change wpm, but it is what
makes the session feel unhurried: the dwell time lives in the gaps between
phrases rather than in stretched phonemes. To slow the voice itself further,
lower `--stretch` — 0.7 reaches roughly 115 wpm. Below about 0.7, `atempo`
starts to smear sustained vowels, which is exactly where this script lingers.
Re-tuning costs no API calls, since stretch is applied after the cache.

## Clean joins and exact pauses

Two defects that a segment-and-assemble pipeline invites, and how the tool
avoids them:

**Clicks.** ElevenLabs' `next_text` parameter tells the model that more speech
follows immediately. That is false here — seconds of silence follow — so the
segment ended mid-decay at full amplitude, and appending digital silence
produced an audible click. It affected 22 of 84 segments. The tool now sends
`previous_text` only, and additionally fades each segment's edges (10 ms in,
30 ms out), so nothing can end on a discontinuity.

**Pauses longer than written.** The engine pads each segment with its own
leading and trailing silence — up to 1.15 s, 46 s across the session — which
silently stretched every gap. Each segment is now trimmed to its speech, plus
a 50 ms tail, before the scripted pause is laid down. Measured gap error
against the script is 0.02 s mean. Pass `--no-trim` to keep the padding.
