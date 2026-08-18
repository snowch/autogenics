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
| Finished (film) | [`script/finished.md`](script/finished.md) | [`video/finished.mp4`](video/finished.mp4) | 1:08 |
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
python3 tools/test_gate.py     # behavioural: does the gate open for the right reasons?
python3 tools/build_pwa.py
```

`check_app.py` parses the inline scripts with `node --check`, then **checks
them concatenated**, which is how the browser actually runs them: a `var` in
one and a `let` of the same name in another is a SyntaxError that kills the
second script outright, and checking each in isolation sees nothing. That is
exactly how the service-worker registration went silently dead — `var timer`
against the app's `let timer` — leaving a PWA with no worker at all. It also
verifies that
every `$('#id')` resolves, every audio key is defined, that **no local variable
shadows a top-level function** — `const go = …` inside `renderJourney` quietly
turned every `go('progress')` in that scope into a DOM element, which is valid
JavaScript and invisible to a syntax check — and that **Reset really
resets** — that it clears `onboarded`, and that it clears every state key a
fresh install starts with. It once set `onboarded:true`, so "start again from
the beginning" wiped the record but skipped first run and left the user standing
on the screen they had pressed the button from. The second half of that check is
the one that matters over time: a new state key added to the loader and
forgotten in the reset leaves stale data behind a wipe. A malformed string
literal takes out the entire script block and leaves a page that renders but
does nothing — grepping the HTML will not catch it, and one shipped that way.

It also refuses **a block that appears twice**. Inserting the settings screen
with an anchor that happened to match three times pasted `applyTheme()`, the
theme-button wiring and the build stamp into the step-advance handler and the
reset handler as well as at the top level, and it shipped: forty-eight dead
lines, and a theme control silently rewired on every step advance. Nested
function declarations are legal and identical copies parse, so nothing above
saw it. Two greps do — a function declared more than once, or a long comment
appearing more than once, means a block was pasted more than once. The same
edit tried it again on the nidra runner and was caught before the commit.

### The app says which build it is

Under *Your record*, quietly: `Build 4958f0a`. The short commit the PWA was
built from, stamped in by `build_pwa.py`, with a `+` when the tree was dirty.

It exists because a deploy that failed and a service worker that never updated
look identical from the device — both show yesterday's app — and there was no
way to tell them apart without going to the Actions tab. A Pages deploy did
fail with a 503, the previous build stayed live, and the first explanation
reached for was the worker. The stamp answers it in one look.

### Updates land without clearing site data

The worker `skipWaiting()`s and claims clients, so a deploy activates — but the
page already on screen keeps rendering the HTML it loaded, and an installed PWA
is almost never navigated away from. The result was a user sitting on a stale
build with no way forward except clearing site data by hand.

**It never reloads during a practice.** Someone is lying down with their eyes
shut for ninety seconds; restarting the app under them is the one moment this
must not happen. A waiting update holds while the practice screen, a film, or
the rating screen is up, and lands the moment the user leaves it. Found by
running the case rather than reasoning about it — the first version reloaded
straight out of a running timer.

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
python3 tools/build_app_artifact.py --standalone   # -> build/autogenics.html
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

### The app was still called Heaviness

The tab title, the manifest name and the home-screen label all said
*Heaviness* — the name from when heaviness was the only exercise it taught. Ten
steps and six exercises later, a bookmark was advertising the first week.

**Autogenic Training** for the tab and the manifest, because that is what
someone will recognise it as in a bookmark list, and **Autogenics** for the
home screen, which truncates. The single-file build is `autogenics.html` for
the same reason.

Worth noting the audience split here: the positioning aims at people who tried
meditation and stopped, who may not know the term — but by the time this is on
a home screen they have installed it, and recognising what it is beats pitching
to them again. The pitch belongs in a store listing.

### A settings screen behind the gear

*Your record* was in Learn, where it had nothing to do with learning, and there
was no way to choose a theme at all — the app followed `prefers-color-scheme`
and that was that. Both now live on a settings screen opened from a gear in the
header, which keeps the tab bar at three: Practice, Progress, Learn are the
things you do, and settings is not one of them.

The theme choice is System, Light or Dark, stored with the record, applied to
`data-theme` and to the `theme-color` meta so the status bar follows. It
survives a reset — someone wiping their practice record has not asked to be
thrown back to the system theme.

### Progression is calendar-paced, and our floor disagreed with our film

Every trial of this method that reports its schedule runs **eight weekly
sessions**, one exercise per session — Kanji 2006, Bowden 2012, Ramirez-Garcia
2023 — and the standard text has heaviness arriving "within a week". Taught
courses pace by the calendar; "do not add the next formula until the last comes
readily" is advice rather than a gate.

Our gate is a hybrid and stays one, because criterion alone lets people stall
forever and time alone stacks formulae on a response that never established.
But the floor was **five days** while the intro film says "about a week on
each" — the app contradicted its own narration and let someone advance faster
than any instructor-led course allows. It is seven now.

### Contrast and tap targets, measured

Never checked until it was, and light theme was failing badly: `--muted` at
2.53:1 against white where 4.5 is the floor, and the accent at 3.56:1 on its own
soft background. Dark was marginal — 3.72:1 on the small pills.

Fixed by computation rather than by eye. Each token was tested against every
surface it actually sits on and walked toward the background, scaling its
channels proportionally so the hue survives, until it cleared 4.6:1. Light
`--muted` #8394A4 → #546474, `--accent` #B0682F → #955827, `--good` → #366C58;
dark `--muted` #6F8090 → #8192A2. Every screen in both themes is clean.

Tap targets: the guided/timer switch was 38px, a path row 28px, the cautions
link 18px. Now 44px, 44px, and 24px.

One caution about the audit itself. Its first run flagged the nav labels at
3.58:1, which was the audit's bug, not the app's: `color-mix()` computes to
`color(srgb 1 1 1 / 0.92)` and a naive number-grab reads "1 1 1" as near-black.
A measurement you have not checked is just a more confident guess.

### Practice, Progress, Learn

An earlier version had a Today tab beside a Progress tab, and it was removed:
"today" was just the open step, so the two screens duplicated the same state
and the path got hidden behind the duplicate.

The split is back, on a different line, and the difference is that there is no
duplication. **Practice is what to do now** — one hero, and nothing else that
scrolls. **Progress is how it is going** — the fourteen-day record, the two
conditions for moving on, and the path with its repeat and replay. Those are
retrospective, and they always sat awkwardly under a hero whose whole job is
"one thing, now". By the last step the practice screen had grown to a hero plus
a record plus ten path rows.

The gate moving to another tab creates one risk: the app silently waits for
someone to go looking. So the two moments that actually change what the user
does — *ready to move on* and *finished* — surface on the practice screen as a
short card that links across. And advancing a step returns to Practice, because
what changed is what to practise; guided mode comes back on with the new phrase.

Three tabs, and the middle one earns its place now that the path is navigable
rather than a list.

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

### Inserting a step renumbered the recordings

Adding legs at position four pushed everything after it down one, and every
later recording says its own number out loud — "Step four. Heaviness is yours
now, so we add warmth." The screen said STEP 5 while the voice said step four,
for five consecutive steps, and nothing caught it because the scripts were
internally consistent. All five renumbered and re-rendered.

The same sweep found the forehead step showing an on-screen cue, *my arms and
legs are heavy and warm*, that the recording never says — it says the two lines
separately. That came from a bulk edit of the cue arrays that did not check
itself against the scripts.

`check_app.py` now does check: for every step with audio, each cue must be a
line its script actually speaks. It caught the forehead mismatch on its first
run, and then caught the two stale builds that had not yet been regenerated.

While in that script, the cool-forehead imagery — *as though a window had been
opened somewhere in the room* — was sitting before the heaviness recap, four
formulae before the one it describes. It now sits with it.

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

### Timer mode never told you how to finish

Guided tracks walk the take-back. Timer mode reserved the last fourteen seconds
for it and changed the heading to "Waking up" — while the cue underneath still
read *I am completely calm*. No instruction at all, in the one part the
cautions call non-optional and the onboarding promises the app always runs.

The last fifteen seconds now carry it: bend and stretch, a deep breath, open
your eyes. The practice cues are spread across the remaining time rather than
the whole duration, so they no longer run into it.

### The dose is ninety seconds of practice, not ninety of everything

Measured off the example track's own timings rather than assumed:

| | |
| --- | --- |
| settle → last "completely calm" | 79.8s |
| take-back | 21.9s |
| six repetitions, 4s apart | 38.5s of that |
| formula delivery | 121 words/min |

So ninety seconds is comfortably enough for the practice proper — six
repetitions at an unhurried pace only fill 38 of it — and the take-back is
fifteen on top, which is how the copy already describes it. The app's timer
budgets 96–104s per step, which is the two added together.

**No pauses inside the phrase.** The gap belongs *between* repetitions, and at
four seconds it is longer than the phrase itself. Breaking *my right arm is
heavy* into separate words would turn the formula into something you assemble,
and assembling it is the effortful attention the whole method is trying to
avoid. It should pass through and be let go.

### Finishing the day is a moment

Three practices a day is the entire mechanism, and hitting it was never
acknowledged — the button just changed to "Practise again", which reads as *not
enough yet*. Once the day's three are in, the eyebrow says **Done today**, a
line says so plainly, and the primary action steps down to a ghost labelled
"Practise anyway". More is not better here, and a product built on short and
often should not push for a fourth.

### The record belongs to the step it describes

Progress used to be a record card floating above a path. The card is *about*
the current step — its fourteen days, its two conditions, its move-on button —
and the step it described was not even on the path: the list ran from the last
finished step straight to the one after the current one, so on day one it
showed an intro and a NEXT and nothing you were actually doing.

The current step is on the path now, marked NOW, and the record hangs off it,
open. The path is the whole page: intro, what is done, what you are on with its
record, what is next.

Three bugs surfaced doing it. `li.step now` collided with `.now`, the hero
card's class, so a row of the list wore a surface, a border and a shadow.
`'Day '+n+' · '+a+b` concatenated where it meant to add, printing "00 of 2".
And `el('h2', 'Ready to move on?')` passed the heading as the *class* argument
— that card's heading has never once rendered, and only showed up because a
scripted check read its text and got an empty string.

The strip is seven days rather than fourteen. Forty-two cells is a lot of chart
to sit inside a list row, the three-a-day rows are the part worth keeping since
they teach the dose, and the gate never looks back further than five days
anyway.

### Naming the thing instead of pointing at it

Two lines said "it" where the word was doing real work. The debrief opened on
"That's one." — one what? — and the example track said "Do it with me" before
the listener knew what *it* was. Now "That's one practice." and "Practise with
me", which also puts the example in the repo's own grammar: practice the noun,
practise the verb.

### A briefing you have watched is still findable

Replay hung only off *finished* steps, so a film about the step you are on was
unreachable for the entire week it applied to. Worst on day one: the after-first
debrief belongs to step 0, so watching it made it vanish for a week — the card
offered it, dismissal was recorded, and nothing anywhere could bring it back.

The current step's panel carries its films too, named, with the button reading
Watch or Watch again depending on whether it has been seen. The lookup moved
from `find` to `filter` while it was open: one film per step today, but `find`
would have silently hidden the second.

### Every film replays from the path

Replay used to be in two places: the intro under Learn, the briefings on the
path. One kind of thing, two places to look.

The path is the journey, so it carries all of them in the order they were met
— the programme intro at the head, each exercise's briefing on its own step,
the closing film at the tail once it has been earned. Learn keeps the method
and loses the journey.

What did **not** move is a briefing's *first* showing. That stays on Practice,
because its entire value is timing: it appears when you arrive at a new
exercise, before your first go at it. Behind another tab nobody meets it at the
moment it is for, which is the whole reason it stopped being a four-minute
lecture up front.

Which leaves the question of whether "Practice" is the right name for a screen
that sometimes offers a film. It is: the screen is the current step, and a
briefing about the current step is the current thing to do. Renaming it to
Focus or Now buys vagueness — "Practice, Progress, Learn" says what each screen
holds, and the film is a minute of the practice you are about to start.

### The ladder has an ending now

The first screen promises you end up not needing this, and until now nothing
ever said so: the last step ran forever, its gate permanently unmet because
there was no next step to unlock. Someone who learned the whole method got no
acknowledgement of it.

The same two criteria that open every other step now close the last one — five
days at it, landing twice a day for three days running. Meeting them shows
**Finished**, and offers a closing film about what the method is for once you
can do it unaided, and the one thing that undoes it.

It is deliberately not a celebration: no badge, no streak saved, no confetti.
The tone is a handover. Anything triumphant would sit badly on a method whose
entire skill is not making a fuss, and on a product that has spent nine steps
promising to get out of the way.

While looking at that screen: the hint under the phrase read "say it silently,
in your own voice" beneath *All six, in sequence* — which is not a phrase
anybody says. The final step gets its own.

### Look ahead, but never advance

The gate is the one thing that makes this better than a syllabus, so there is
no way to skip a step. But that left the whole programme invisible: on day one
you could see day one, and nothing else. Wanting to know what is coming is not
the same as wanting to be given it, and refusing both is a design mistake
dressed up as rigour.

Settings now lists every step and drops you into it — running on an invented
record, in a sandbox. The trick is a single line: `save()` returns early while
previewing. Everything downstream keeps working exactly as it does normally —
ratings, the gate, the probe, skipping, the weekly question, the shrinking cues
— and none of it survives leaving. Nothing else in the app knows it is in a
sandbox.

Each step gets two moments, because a step is not one screen. *Just arrived* is
where the regression note, the cautions and the discharge reminder live; *a
week in* is where the gate, the probe and the shrunken cues are. Previewing one
would show half the content and imply the other half does not exist.

A fixed 56px nav offset for the preview bar was wrong the moment the label
wrapped to two lines, so the bar measures itself and sets the offset. This is
the third layout bug this session caused by guessing a size instead of asking
for one.

### The ending is a handover, so make it leave

**No digits during a practice.** A countdown is something to check, and
checking is a mild form of trying — the one thing the method says not to do.
The ring still turns; there is simply nothing to measure yourself against.
Gone from the nidra runner too, except the sleep variant, where counting up is
the only readout there is.

**A countdown that falls.** The path header now reads *"4 done · about 11 weeks
left at your pace"*, computed from the days they have actually practised rather
than a nominal schedule. It is the only number in the app that is supposed to
decrease, and it makes the first screen's promise concrete in week five instead
of week ten.

**The deliverable leaves the app.** Finishing offers the sequence as a
1080×1920 PNG for a lock screen — six formulae, no branding, no link back here,
and skipped exercises left out of it. A product that spends nine steps
promising to get out of the way should be willing to make the ending portable.

**Nidra moved out of Settings to the end.** Someone on step two has an entry
technique they cannot yet issue and no reason to want somewhere to put it, and
offering a second practice contradicts the one-thing-at-a-time discipline that
is the whole of what autogenic training contributes to that graft. It appears
once the ladder is done — or if it has already been used, since taking a thing
away from someone using it is worse than having offered it early. Settings is
where features go when nobody has decided what they are, and this one now has
a place.

### The middle of the programme has a design now

Six changes, all from `DESIGN.md` §7, all about the weeks where the novelty has
gone and the finish is not in sight.

**Lapses.** Five days away or more offers one session of the last element you
had solid, then the current phrase afterwards. It never shows what was missed —
the record shows density, and a gap is allowed to be unremarkable. Returning
cold onto the hardest current material is how a lapse becomes a stop.

**The regression.** Every step up feels like a step down, six times over. The
app now says so on a new step, using the record: *"Warmth took you 7 days, and
you are on day 1 of this one."* A generic reassurance is weak; their own
history is not, and it gets stronger every step.

**A halfway mark.** Nine weeks with one acknowledgement at the very end is too
long. The landmark is not the numerical middle but the end of warmth —
heaviness and warmth are the two that do most of the work and carry most of
what evidence exists. Same handover tone as the ending, no celebration.

**Discharge, again, where it happens.** It was explained once after the first
practice and then not mentioned for six weeks, by which point you are at the
warm centre and the cool head, which is exactly where unexpected emotion turns
up. Re-surfaced there.

**A dignified exit from the cautioned steps.** The heartbeat and the warm
centre are traditionally taught in person, and the cool head says outright that
stopping at the first five is fine — but the path assumed all ten, so somebody
correctly told to avoid an exercise could only stall against it. Skipping is
allowed, the skipped formula is then dropped from every sequence that would
have gone on instructing it, and the review never draws it.

**One weekly question.** *Compared with last week — easier, the same, or
harder?* Daily ratings are for the gate; the signal that detects a plateau is
weekly and comparative, and nothing in the daily log surfaces it.

### Three practices, a probe, and a shrinking cue

Three changes from `DESIGN.md` that together make the middle of the programme a
design rather than a syllabus.

**The day is no longer three of the same practice.** The stack three times over
gave the element being learned two of eight cue slots by the eighth step, while
five consolidated ones took the rest. It is now the phrase alone, one earlier
element in rotation, and the stack once — six exposures for the new formula
instead of two, and somewhere for the old ones to be rehearsed rather than
recited. It splits only off the guided track, since no recording exists of a
phrase alone. A review is logged against the step it revisited, which keeps the
two-a-day evidence rule meaning what it did.

**The gate has a third criterion.** Days and ratings both describe a session
with cues on screen or a voice in your ear, so they measure the response with
the scaffolding still holding it up. The probe is the same length with nothing
at all — one note to begin, one to finish — and it is the only thing that
catches a formula which has quietly become recitation. Offered only once the
other two are met, because a probe you cannot pass yet is a way of telling
someone they are failing.

**Cues shrink as they consolidate.** `My right arm is heavy.` → `Right arm,
heavy.` → `Heavy.`, keyed to how many days you have actually been saying that
line, counted from the record. Inside one sequence the old elements are down to
a word while the one being learned is still a whole sentence, which is exactly
the right shape. Never applied to a guided session, where the cues have to
match what the recording says.

### Reminders, without a server

Three practices a day is the entire method, and the app had no way to ask for
any of them. The obvious fix is push notifications, and it is not available:
web push needs a backend and an identity, which this app has spent its whole
design refusing; notification triggers never shipped; periodic background sync
is Chrome-only and twelve-hourly at best. A native wrapper would solve it, and
that is a real answer, but not one you can act on this week.

The phone already contains a reliable scheduler that runs offline, survives
reboots, and nobody has to be talked into trusting. Settings now takes three
times and hands the calendar an `.ics` — three daily repeating two-minute
events, each with an alarm, generated on the device and passed straight to the
calendar app. Floating local time on purpose, so half past seven stays half
past seven in another country.

Verified by generating one in the browser, reading the download back, and
parsing it with an RFC 5545 parser: three events, daily recurrence, one alarm
each, CRLF throughout — which the spec requires and real parsers enforce.

The times are a setting, not a practice record, so they survive Reset the way
the theme does. And three time pickers side by side overflowed the card and
scrolled the whole page sideways on a 390px screen, because a 12-hour locale
renders AM/PM and a clock affordance in each one. They are stacked now.

### The take-back was silent, and the screen went to sleep

Two bugs that only exist in real use, found by thinking about what the app does
on a phone lying on a chest for ninety seconds with the eyes shut.

**The take-back had no sound.** In timer mode its three cues changed on screen
and nowhere else. The cautions call the take-back non-optional and the
onboarding promises the app always runs it — and it was running it as text, to
somebody who is not looking. It now has two rising notes at the boundary, and
the practice card says what they mean where the mode is chosen: one note to
begin, two rising to come back, two low when done.

**Nothing held the screen awake.** Every phone's screen timeout is shorter than
a practice. A sleeping screen throttles or freezes `setInterval`, which is what
fires the chimes, so the longer the session the more likely it ended in silence
— and the twelve-minute nidra runner, where the chimes *are* the instruction,
was the worst case. Two fixes, because either alone is thin: a screen wake lock
held for the duration and re-taken when the page comes back, and every tone
scheduled on the Web Audio clock at session start rather than fired by the
interval. The audio clock keeps time whether or not the JS timer runs. Verified
by reading the schedule back: `0, 81, 81.3, 96, 96.5` for a 96-second step, and
the nine nidra boundaries at `30, 120, 150, 210, 300, 480, 600, 690, 720`.

Scheduling ahead brings its own bug, so `hush()` cancels the pending
oscillators when a practice is cancelled or a nidra session stopped. Otherwise
the app chimes at you a minute after you walked away.

### Absence used to count as practice

The gate has two halves: at least seven days on the phrase, and evidence it is
landing. The second half was doing all the work, because the first was
measuring the wrong thing — `stepDays()` returned calendar days since the step
opened, so a lapse counted as progress. Two sessions, three weeks away, three
good days on return, and a gate that means "about a week on this phrase" opened
on six days of practice spread over twenty-four. Six honest days passed it too,
for the same reason.

It now counts days on which something was actually logged for this step. The
same change makes lapses behave sensibly everywhere else: a fortnight away
neither advances you nor punishes you, it simply does not count, which is the
only defensible reading of a criterion-referenced gate.

`guidedDefault()` moved to the same footing — the first three days you turn up,
not the first three on the calendar, so someone practising on days 1, 5 and 9
still gets guided through all three. It reads the days *behind* today rather
than including it, because counting today flipped the mode partway through the
third day, between one practice and the next.

This is the class of bug `check_app.py` cannot see: the code parsed cleanly
whichever thing it counted. So `tools/test_gate.py` loads the real app in a
browser and asks `gate()` what it thinks about six scenarios — the lapse
exploit, an honest week, six days, once-a-day, faint ratings, and landing that
happened but has since stopped. Run against the commit before the fix it
reports two failures. It is the first behavioural test in the repository and
there should be more of them.

### The nidra runner is silent, and that is the whole point

`PRIMED-NIDRA.md` argues that autogenic training and yoga nidra each fix the
other's main defect: nidra has content but no training method, AT has a
training method but its six exercises are all induction and no content. The
argument is only worth anything if the graft can be built, and the piece that
tests it is small — a **silent staged timer**, under Settings, marked
experimental.

Silence is the substance, not a limitation. Every nidra tool is a recording,
and a recording is precisely what the protocol removes: a recording carries on
whether or not anyone is still listening, which is why people fall asleep in
the middle of one and call it a practice. A sequence you issue to yourself
stops when you do. So the runner chimes at each stage boundary, shows a cue
rather than narration, and never speaks.

Three lengths: 12 minutes tiling nine stages exactly, a 3-minute field version,
and a sleep version that counts *up* with no arc, no cancellation stage and no
ending — you are meant to fall asleep in it, so it does not count towards
anything. Cue wording shrinks with completed sessions (full under 8, compressed
under 20, one word after), because the endpoint of consolidation is an
instruction small enough to cost nothing to issue. The opposites pair advances
one step per session, so the nine cycle rather than being chosen.

The length segment and the Begin button are separate controls. They were one at
first, which put a tap that starts twelve minutes of silence in the same visual
language as a theme preference — and a settings screen is somewhere people poke
at things to find out what they do.

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
