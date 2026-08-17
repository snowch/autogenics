# autogenics

### [→ Open the app](https://snowch.github.io/autogenics/)

Installable on Android and iPhone, and it runs offline after the first load.
No account, no backend; the practice record stays on the device.

Scripts and guided-audio recordings for **autogenic training** — the six
standard exercises.

The written script is the single source of truth. The audio is rendered from it
by `tools/generate_audio.py`, so the recording can never drift from the text:
edit the markdown, re-run the tool.

## Sessions

| Track | Script | Recording | Length |
| --- | --- | --- | --- |
| After your first practice (film) | [`script/after-first.md`](script/after-first.md) | [`video/after-first.mp4`](video/after-first.mp4) | 1:41 |
| Briefing — warmth (film) | [`script/brief-warmth.md`](script/brief-warmth.md) | [`video/brief-warmth.mp4`](video/brief-warmth.mp4) | 0:58 |
| Briefing — heartbeat (film) | [`script/brief-heartbeat.md`](script/brief-heartbeat.md) | [`video/brief-heartbeat.mp4`](video/brief-heartbeat.mp4) | 1:08 |
| Briefing — breathing (film) | [`script/brief-breathing.md`](script/brief-breathing.md) | [`video/brief-breathing.mp4`](video/brief-breathing.mp4) | 0:52 |
| Briefing — warm centre (film) | [`script/brief-solar.md`](script/brief-solar.md) | [`video/brief-solar.mp4`](video/brief-solar.mp4) | 1:04 |
| Briefing — cool head (film) | [`script/brief-forehead.md`](script/brief-forehead.md) | [`video/brief-forehead.mp4`](video/brief-forehead.mp4) | 0:55 |
| **Stage 1 — right arm** | [`script/arm-heaviness-example.md`](script/arm-heaviness-example.md) | [`audio/arm-heaviness-example.mp3`](audio/arm-heaviness-example.mp3) | 2:32 |
| **Stage 2 — both arms, in turn** | [`script/arm-heaviness-example-2.md`](script/arm-heaviness-example-2.md) | [`audio/arm-heaviness-example-2.mp3`](audio/arm-heaviness-example-2.mp3) | 2:15 |
| **Stage 3 — both arms together** | [`script/arm-heaviness-example-3.md`](script/arm-heaviness-example-3.md) | [`audio/arm-heaviness-example-3.mp3`](audio/arm-heaviness-example-3.mp3) | 2:05 |
| **Heaviness — legs, step 4** | [`script/at-heaviness-legs.md`](script/at-heaviness-legs.md) | [`audio/at-heaviness-legs.mp3`](audio/at-heaviness-legs.mp3) | 1:48 |
| Warmth — step 5 | [`script/at-warmth.md`](script/at-warmth.md) | [`audio/at-warmth.mp3`](audio/at-warmth.mp3) | 1:54 |
| Heartbeat — step 6 | [`script/at-heartbeat.md`](script/at-heartbeat.md) | [`audio/at-heartbeat.mp3`](audio/at-heartbeat.mp3) | 1:57 |
| Breathing — step 7 | [`script/at-breathing.md`](script/at-breathing.md) | [`audio/at-breathing.mp3`](audio/at-breathing.mp3) | 1:54 |
| Warm centre — step 8 | [`script/at-solar-plexus.md`](script/at-solar-plexus.md) | [`audio/at-solar-plexus.mp3`](audio/at-solar-plexus.mp3) | 2:03 |
| Cool head — step 9 | [`script/at-forehead.md`](script/at-forehead.md) | [`audio/at-forehead.mp3`](audio/at-forehead.mp3) | 2:00 |

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

The first one is built: [`video/intro.mp4`](video/intro.mp4), 2m 09s, eighteen
slides, from [`script/intro.md`](script/intro.md).

```bash
python3 tools/generate_audio.py script/intro.md -o audio/intro.mp3 \
    --timings build/intro-timings.json
python3 tools/build_video.py video/intro-slides.json \
    --timings build/intro-timings.json --audio audio/intro.mp3 \
    --out video/intro.mp4
```

`--timings` writes each spoken line's start and end; each slide names the last
line it covers, so cuts land on the narration. Measured drift between audio and
video on the built file: 0.00s.

**Slides anchor the narration, they do not repeat it.** The first cut of this
deck put the spoken sentence on screen as it was spoken — twelve of eighteen
slides were near-verbatim transcripts. Identical text and speech compete rather
than reinforce: reading and speaking run at different speeds, so the viewer ends
up doing both badly. Every slide is now six words or fewer, and the ones that
carry weight are structural rather than textual — the phrase itself, the ladder,
the dose. Two exceptions are deliberate: "Guided. Then a timer. Then nothing."
condenses three sentences into a rhythm, and "You end up not needing this." is
the thesis and worth landing on screen as it is said.

Posters are written by `--poster` during the video build, from the middle of a
named slide (the formula, by default) rather than frame one — frame one is a
title card, and the poster is what invites the tap. Generating them in the build
is the point: one shipped showing a slide that had since been edited, and
nothing noticed until the screen was looked at.

First run runs **invitation → what it asks → film → cautions → start**, in
that order. The invitation and the dose were one panel until a phone
screenshot showed it running edge to edge with nothing to breathe; the ask
and the fact that it ends now get their own page.

Safety was originally the first screen, on the reasoning that it is the
responsible place for it. It made the app open on "not medical treatment",
"never while driving" and "see a doctor" — which reads as a consent form and is
a poor thing to meet before you know what the app is for. The cautions now sit
immediately before the first practice, where they are still unavoidable and no
longer the greeting. They also lead with the practical points and keep the
medical disclaimer quiet at the bottom, since only one of those is a warning
the practitioner acts on.

The cautions stay **text with an explicit tap to continue**, never video: a
film can be skipped, muted, or half-watched, and "they were told in a video" is
a weaker position than "they tapped to acknowledge".

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
every `$('#id')` resolves, every audio key is defined, and that **Reset really
resets** — that it clears `onboarded`, and that it clears every state key a
fresh install starts with. It once set `onboarded:true`, so "start again from
the beginning" wiped the record but skipped first run and left the user standing
on the screen they had pressed the button from. The second half of that check is
the one that matters over time: a new state key added to the loader and
forgotten in the reset leaves stale data behind a wipe. A malformed string
literal takes out the entire script block and leaves a page that renders but
does nothing — grepping the HTML will not catch it, and one shipped that way.

### Updates land without clearing site data

The worker `skipWaiting()`s and claims clients, so a deploy activates — but the
page already on screen keeps rendering the HTML it loaded, and an installed PWA
is almost never navigated away from. The result was a user sitting on a stale
build with no way forward except clearing site data by hand.

Registration now checks for a new worker on launch **and on resume**
(`visibilitychange`), and reloads once when a new worker takes over. The flag
guarding that reload is a running one rather than a snapshot: read once at load
it is false on a first-ever visit, stays false when that first worker claims the
page, and then swallows the reload for the genuine update that follows. That is
exactly what the first version did, and it took a scripted deploy-while-open
test to catch — the caches had rotated correctly, so everything looked right
except the screen.

Tested by serving a copy of `docs/`, loading it, editing `index.html` and the
worker's cache name underneath the open page, then firing a resume: the page
reloads itself into the new build and the old cache is gone.

It is committed, so **GitHub Pages serves it as-is**, live at
**<https://snowch.github.io/autogenics/>**: repository *Settings → Pages →
Source: Deploy from a branch → this branch, folder `/docs`*. Any static host
works too — the directory has no build step and no backend.

Point it at **`main`**, folder **`/docs`**. The folder matters: left on
`/ (root)`, Pages renders the README as the landing page instead of the app. A
root [`index.html`](index.html) redirects to `./docs/` so that case still lands
on the app rather than on documentation, but `/docs` is the setting to use —
it publishes only what is meant to be public rather than the whole repository.

Renaming or deleting the branch Pages builds from switches the site off
(`has_pages` flips to false), so it has to be re-enabled afterwards.

The published directory is verified before it ships by serving it over real
HTTP and driving it with the bundled Chromium — service worker registration,
a full precache, then a reload with the network switched off. `*.github.io` is
blocked by this environment's egress policy, so the deployed site itself cannot
be checked from here; the local HTTP run is the closest available stand-in.

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
python3 tools/shoot_app.py                        # screenshot the screens
python3 tools/build_app_artifact.py --standalone   # -> build/heaviness.html
```

`build_app_artifact.py` inlines everything as data URIs, and re-encodes the
films to half resolution on the way in. Seven of them at full size pushed the
single file past 17 MB, which is a poor thing to open on a phone; at 540px they
come to 11 MB and the typography is still crisp, checked by extracting a frame
and looking at it rather than assuming. The PWA keeps the full-quality
originals — this copy exists only because everything has to fit in one file.

`shoot_app.py` renders each screen with the bundled Chromium at phone size,
including a seeded mid-ladder state, into `build/shots/`. That now covers the
running practice, the rating, and the briefing player — three surfaces that had
never once been looked at, and one of which was showing a stale poster. The design faults in
this app were consistently found by looking at it and consistently missed by
inspecting the markup, so look at it.

### Progress shown as achievement, not backlog

The practice screen lists **only steps you have finished**, under "Done so
far", and shows nothing at all on day one. It previously listed all nine with
the unreached ones marked *Later*, which on a first run is eight things you
have not done — a backlog, before you have practised once.

The full six-exercise arc is still shown, but in the intro film and under
Learn, where it reads as a map rather than a debt. The header counts the step
you are on rather than the steps remaining, and the advance button appears only
when the criteria are met, since a permanently disabled button reads as broken
rather than as "not yet".

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

### A path, but not an endless one

Finished steps used to be a read-only list. They are now a path you can
navigate: tap any completed step to see its phrase, practise it again, or
replay its briefing. That is the reason a path earns its place here — and the
reason it did not earn it before, when there was nothing to go back to.

It shows everything finished plus **exactly one step ahead**, named, with
"opens when this one lands". Not the remaining nine. The earlier decision that
a wall of untouched steps reads as a backlog still holds; what changed is that
a path is now navigation rather than a preview.

Deliberately **not** Duolingo-shaped, despite the obvious resemblance of the
problem. Locked nodes, streak counters and an endless scroll of future units
are retention machinery for a product designed never to finish. This one is
designed to finish — guided, then a timer, then nothing — and borrowing that
visual language would quietly promise the opposite of the thing being sold.

**Revision is not logged.** Practising an old step runs its audio and cues and
then simply ends: no rating, no entry. Letting it fill one of today's three
slots, or count toward a gate on a phrase it was not practising, would corrupt
the one record the app asks the user to trust — and the gate is the only reason
that record exists.

### The legs were missing

The ladder went right arm, left arm, both arms, then straight to warmth. That
quietly dropped half of the first standard exercise: heaviness in autogenic
training is a *limb* response, and the consolidated formula names both — *my
arms and legs are heavy*. Wikipedia's Technique section, citing Lehrer,
Woolfolk & Sime's *Principles and Practice of Stress Management*, puts it
plainly: "within a week, a short concentration can trigger the sensation of
heaviness in a trainee's arms and legs."

**One step, not three.** The orthodox progression would be right leg, left leg,
both legs, then the consolidation — which would add a fortnight to the ladder
and teach nothing new. The three arm steps exist because that is where the
skill is learned: holding a phrase without effort, noticing rather than
producing. Once that is in place the response generalises, which is what the
literature describes. Warmth was already compressed to a single step on exactly
this reasoning; legs now match it. Nine steps became ten.

Every later track recaps heaviness before adding its own formula, so all five
were re-rendered to say *my arms and legs are heavy*. Leaving them would have
put the guided cue and the voice out of step — the one failure this pipeline
exists to prevent.

### Every exercise introduces itself

There is a briefing for each step that starts a **new** exercise — warmth,
heartbeat, breathing, warm centre, cool head — plus the debrief after the first
practice. Around a minute each, offered when you arrive at the step and before
its first practice, and replayable from the path afterwards.

No briefing for heaviness in the legs: it continues an exercise already
running, and a film that said "same again, lower down" would be noise.

This is what let the **explainer go entirely**. Four minutes of upfront teaching
before the user had felt anything was answering questions nobody holds yet, and
every part of it now lands where it applies: why heaviness and what counts, in
the debrief; each exercise's own mechanics, in its briefing; the take-back and
the cautions, on the safety card. Learn lost its second pane with it and is one
flat page again.

### Briefings are offered after the moment, not before it

The old explainer front-loaded four minutes of teaching before the user had
felt anything. Half of it answers a question nobody holds yet: "what was I
supposed to feel?" is not a real question until you have sat there for ninety
seconds and, most likely, felt nothing.

So that half is now a film offered **after the first logged practice**, from a
card above the hero. It is an offer, with *Watch* and *Not now* — never an
autoplay. Someone who has just finished a relaxation exercise may be about to
stand up and leave, and seizing that moment would undo the thing being
explained. Dismissal is recorded in `S.briefed`, so it never asks twice.

`BRIEFS` is a list with a `when(S)` predicate; step briefings get a default
predicate of "you are on this step and have not practised it yet", so adding one
is a row rather than a feature.

Verification note: the bundled Chromium reports `''` for `canPlayType` on H.264,
because open-source builds ship without proprietary codecs. Films therefore
cannot be decoded in this environment and `readyState` stays 0 — a limitation of
the test browser, not of the app, since Chrome on Android and Safari both handle
H.264. What is checked instead is that each briefing surfaces, resolves to the
right file, and that the file is served — including from cache with the network
off.

Adding a film used to mean editing three places — the app's `AUDIO` map,
`build_pwa.py` and `build_app_artifact.py`, each with its own hardcoded
`intro.mp4`. There is now one `FILMS` list in `build_pwa.py` that the artifact
imports, and the artifact no longer keeps a private copy of `TRACKS`.

### Learn is help and method, not one page

Learn was answering two unrelated questions at once — *something is up, what do
I do* and *what is this thing* — and showing both at all times was most of what
made it feel cluttered. It splits on that line, with a segmented control: **Help**
leads, because after the first week it is the only reason anyone opens the tab;
**The method** holds the explainer, the origin, and the record.

Help is the cautions, then *Doing it right* (you cannot make it happen; say it
in your own voice; short and often) and *If it feels wrong* (nothing is
happening; restlessness or emotion). Each pane now fits one screen.

The cautions card is the only surface treatment left on the tab, so it is the
one thing that stands out — but only its two actionable rules are open. The
medical detail and the take-back are collapsed behind them: a twenty-line block
of prose at the top of the page was itself the clutter, however important it is.

### Plain language

User-facing copy avoids terms the reader has no reason to know yet. "Stage"
became "step", "formula" became "phrase", and the take-back is described by
what it does — *finish by waking yourself up* — before it is ever named. The
traditional terms still appear in Learn, glossed on first use, because the
audience for this does eventually meet them in the literature.

### Positioning

**Who this is for:** people who tried to meditate and stopped. Not people
already searching for autogenic training by name — that is a real audience but
a small one in English, and the app used to assume it (the intro video opened
"you already know what autogenic training is", which is now rewritten).

The three pillars, in order of strength:

1. **You finish.** Guided → timer → nothing. The product is designed to be
   uninstalled. No subscription-funded competitor can print this, and it is why
   there are no streaks, no daily engagement mechanics, and a gate that lets you
   leave. Committing to it is a permanent constraint, not a tagline.
2. **You feel it.** A trained physical response — the arm actually gets heavy.
   This answers "am I doing this right?", which is the question meditation never
   answers and the most common reason people quit.
3. **You don't have to try.** Passive concentration: trying is the one thing
   that reliably blocks it. Nothing to concentrate on, nothing to believe in.

**Meditation is the reference point, never a comparison claim.** Talk about its
failure mode — "if meditation never stuck" — never its efficacy. Manzoni 2008
found meditation *outperformed* the relaxation category average, so any
"works better than" framing is one we would lose on the evidence. Mechanism
comparison is fair and true; efficacy comparison is neither.

**Self-hypnosis stays as origin, never as the headline.** It is accurate — the
literature routinely calls AT a method of self-hypnosis — and it earns its place
in Learn as depth. But it is a category rather than a benefit, it connotes being
put under when we are selling deliberate access, and it sets a theatrical
expectation that a slightly heavy arm on day four will not meet.

**"Mind training" is out**, for the same reason brain-performance framing is:
it instructs the user to try, and trying blocks the response. It is also
Headspace's line. The true version is that you *are* training — a physical
response, using words as the instrument. The mind is the tool, not the target.
Where that idea has real pull is agency, and pillar 1 carries it.

### Claims

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

**The method is credited, never the man.** Autogenic training is attributed to
"Berlin in the 1920s" and its originator is not named anywhere a user can see.
That history is now checked and written down in
[`RESEARCH.md`](RESEARCH.md#on-the-founders-name), sourced to Brunner, Schrempf
& Steger 2008 (PMID 19439831): he was assistant director of the Göring Institute
1936–45, publicly advocated compulsory sterilization and the "annihilation of
life unworthy of life", and experimented on homosexual concentration-camp
prisoners. The method's validity does not rest on him. Read that section before
writing anything that reintroduces the name.

**Citing studies is out, for now.** Research on autogenic training exists — it is
reviewed at abstract level in [`RESEARCH.md`](RESEARCH.md), which is a working
record and **not a source for user-facing copy**. Quoting it is the exact move
that turns description into a claim: "studied for X" is read as "helps with X".
The short version of what is there: AT beats doing nothing by a medium effect,
is statistically indistinguishable from every other relaxation method, the trials
are of poor quality, and **no study has tested an app**. If an evidence page is
ever added it belongs under Learn, must carry the second and third of those
findings alongside the first, and every citation must be checked against the
source rather than recalled.

**Cognitive-performance framing is out**, and not only for the legal reason.
"Brain exercise" or "optimal brain performance" would be an enhancement claim,
which is the most heavily policed corner of this market — but worse, it teaches
the wrong thing. Autogenic training runs on *passive* concentration: the one
reliable way to block the response is to try. Framing it as mental training
invites exactly the effort that prevents it, so the copy would be working
against the method.

The honest neighbour is already there: **"a clearer head afterwards"**,
described as what people notice rather than as a faculty being improved.

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
python3 tools/generate_audio.py script/arm-heaviness-example.md \
    -o audio/arm-heaviness-example.mp3
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

python3 tools/generate_audio.py script/arm-heaviness-example.md \
    --engine piper --piper-model voices/en-us-lessac-medium.onnx \
    --bitrate 64k -o audio/arm-heaviness-example.mp3
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
