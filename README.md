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

Seven recordings, and nothing else. Each one is the guided version of a step's
ninety seconds; the app drops to a timer after your first few days and then to
silence, so these are scaffolding with a planned end.

| Step | Script | Recording | Length |
| --- | --- | --- | --- |
| 1 · Heaviness — right arm | [`script/arm-heaviness-example.md`](script/arm-heaviness-example.md) | [`audio/arm-heaviness-example.mp3`](audio/arm-heaviness-example.mp3) | 2:31 |
| 2 · Heaviness — arms and legs | [`script/at-heaviness-all.md`](script/at-heaviness-all.md) | [`audio/at-heaviness-all.mp3`](audio/at-heaviness-all.mp3) | 1:32 |
| 3 · Warmth — hands | [`script/at-warmth.md`](script/at-warmth.md) | [`audio/at-warmth.mp3`](audio/at-warmth.mp3) | 1:51 |
| 4 · Heartbeat — chest | [`script/at-heartbeat.md`](script/at-heartbeat.md) | [`audio/at-heartbeat.mp3`](audio/at-heartbeat.mp3) | 1:54 |
| 5 · Breathing — ribs | [`script/at-breathing.md`](script/at-breathing.md) | [`audio/at-breathing.mp3`](audio/at-breathing.mp3) | 1:51 |
| 6 · Warm centre — abdomen | [`script/at-solar-plexus.md`](script/at-solar-plexus.md) | [`audio/at-solar-plexus.mp3`](audio/at-solar-plexus.mp3) | 2:00 |
| 7 · Cool head — forehead | [`script/at-forehead.md`](script/at-forehead.md) | [`audio/at-forehead.mp3`](audio/at-forehead.mp3) | 1:58 |
| 8 · On your own | — | none, by design | — |

The seven briefing scripts — [`after-first`](script/after-first.md),
[`warmth`](script/brief-warmth.md), [`heartbeat`](script/brief-heartbeat.md),
[`breathing`](script/brief-breathing.md), [`solar`](script/brief-solar.md),
[`forehead`](script/brief-forehead.md), [`finished`](script/finished.md) —
are no longer rendered to anything. They are the source the app's `BRIEFS` text
was written from, and the section below says why.

## The briefings stopped being films

They were seven narrated typographic videos: **7.5 MB of an 11 MB app**, and
they shipped as video only, so the narration could not be heard without also
downloading the slides. Two rounds of argument killed them.

First: a film cannot be skimmed and cannot be heard with your eyes shut, so it
served neither reading nor listening. That suggested audio — and audio was
wrong too, for a reason `DESIGN.md` §1 had already written down:

> Ninety seconds of the interaction is eyes-closed; twenty seconds either side
> is not.

**A briefing is the twenty seconds either side.** It is the eyes-open part, and
the eyes-open part should be read in three seconds, re-readable, and workable in
a waiting room with no headphones. Only the practice is eyes-closed, and only
the practice needs a recording.

So each briefing is a `kick`, a `title`, a one-line `lede` and a `More` fold
carrying the rest of what the narration said. 104–213 words each, which is a
short screen. The app went **11 MB → 3.4 MB**, the ElevenLabs pipeline is needed
only for the seven practice tracks, and a copy change is now a text edit rather
than a re-render — which is what made the intro film go stale twice.

`tools/build_video.py` still works and is left in the tree; nothing calls it.
The slide specs and rendered films are in git history at the commit before this
one if films are ever wanted back.

One thing worth keeping from that pipeline, because it is the same principle
applied to a different surface: **slides anchor narration, they do not repeat
it.** The first cut of the old intro deck put each spoken sentence on screen as
it was spoken, and identical text and speech compete rather than reinforce —
reading and speaking run at different speeds. The text version obeys the same
rule from the other direction: the twenty visible words are a label, and the
instruction is what is behind the fold, not a transcript of it.

### Five of the seven were wired to the wrong exercise

`BRIEFS` carried step numbers written for the ten-step ladder. When the ladder
was cut to eight, `HOPS` was written to migrate the user's saved `S.step` and
nobody migrated these:

| briefing | fired on | which was |
| --- | --- | --- |
| Warmth | 4 | Breathing — ribs |
| Heartbeat | 5 | Warm centre — abdomen |
| Breathing | 6 | Cool head — forehead |
| Warm centre | 7 | On your own |
| Cool head | 8 | **nothing. It never played.** |

That shipped, and nothing noticed — the file parses perfectly either way.
`check_app.py` now refuses a briefing whose step is past the end of the ladder,
or whose id does not name the exercise it fires on, matching against the step's
name, its body part, or a word of its formula. Run against the last standalone
build, the new rule reproduces all six faults.


## Install it on a phone

`docs/` is a complete, installable PWA — the app, compressed audio, icons, a
manifest, and a service worker that precaches everything so practice works
with no signal. Rebuild it with:

```bash
python3 tools/check_app.py     # syntax-check the JS — run this before publishing
python3 tools/test_gate.py     # behavioural: does the gate open for the right reasons?
python3 tools/test_journey.py  # the whole journey in a browser, install to reset
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

### "What this is" was describing one exercise

The screen headed *what this is* said: you repeat a phrase, the arm goes heavy,
it is a physical response. Which is how the **first exercise** works, not what
the product is — and after two rounds of fixing that screen it was still
answering a smaller question than the one it asked.

What it is, is two halves that need each other. Autogenic training is very good
at getting you somewhere and has nothing for you to do once you arrive; yoga
nidra is almost all content and cannot be learned, because it only ever arrives
as a recording to lie down and listen to. That is the whole thesis of
`PRIMED-NIDRA.md`, it is where the name Switch comes from, and until now it was
readable only in Learn, three taps in, after someone had already committed.

So screen one is the shape. It first named the two methods only in a caveat at
the bottom, on the grounds that they are jargon — which does not survive
scrutiny, and was the earlier fix applied mechanically rather than thought
through. Removing *autogenic training* from the kicker was right because it
stood alone as an unexplained label ahead of any reason to care. Naming both
methods as the answer to *what is this* is a different act: it is the specific
claim, the combination is the entire product, and two named traditions carry
more weight than an abstract promise about halves.

The headline names them and the shape follows immediately underneath, so the
specificity comes first and the meaning a line later.

The heaviness mechanism moved to *what it asks*, where it belongs: it is the
concrete how, and it reads better next to ninety seconds and three times a day
than it did standing in for a definition.

### Getting the granularity right

The six tiles were nearly right and had one flaw worth fixing rather than
tidying around. The autogenic column is a real three-level progression, but the
nidra column was not: *Short session* and *For sleep* share a prerequisite, so
a reader scanning three tiles would infer a ladder that had two rungs and a
variant standing in a rung's place.

Two ways out — demote sleep, or build a genuine middle. The middle is the one
that makes the structure true instead of merely honest, so: **seven minutes**,
settle, induction, sankalpa, refuge, pranamaya, opposites, cancellation.

It is not an invented length. The drills arrive in a fixed order — refuge, then
opposites, then counting the breath — so by the breathing step you hold exactly
the three that session needs. Before it there was nothing between three minutes
and the end of the ladder, which is a long gap across precisely the weeks
`DESIGN.md` §7 says have least to look forward to.

Nidra is a three-rung ladder now (3, 7, 12 minutes, opening after refuge,
pranamaya and sakshi), the columns are parallel, and sleep moved to the card as
the variant it always was.

Two things fell out of building it. A nidra tile is gated by a *drill*, not by a
programme, and the two do not line up — the seven-minute session opens at the
warm centre, partway through the deeper four — so the unlock labels had to come
from the drill. And `ndBlocker` returned the *first* unmet requirement when the
one holding a session back is the *last*, which had the seven- and
twelve-minute sessions both claiming to open after opposites when they are four
steps apart.

### Programmes, so the territory is visible

The app had two tracks and a set of prerequisites and no screen that showed
either. The ladder arrived one step at a time, nidra turned up when it turned
up, and the only way to know what existed was to have got there. Progress now
opens on six tiles:

| Autogenic training | Nidra |
|---|---|
| Heaviness and warmth | Short session — three minutes |
| The deeper four | For sleep |
| On your own | Full session — twelve minutes |

Each tile reads *Done*, *In progress*, *Ready*, or the thing that opens it. And
the prerequisites are the argument made visible: **Short session — opens after
heaviness and warmth.** The way you unlock nidra is by doing autogenic
training, which is the entire thesis, stated by the interface rather than in a
paragraph.

It is deliberately not a library. Six tiles, no browsing, nothing to collect,
and a locked tile names its prerequisite instead of disappearing — `DESIGN.md`
§6 forbids a catalogue and this is not one. Practice is still the one thing to
do now; this is the territory that one thing sits in, which is exactly the
split the app was missing.

Tapping an open nidra tile selects that length and drops you on its card;
tapping an autogenic tile goes to Practice; tapping a locked one does nothing
at all rather than explaining itself twice.

### Making the short route visible, and parallel

Opening nidra earlier is no use if nobody finds out. Three changes, and one of
them was already sitting there waiting.

**The halfway landmark and the first nidra unlock fire on the same step.** Not
a coincidence — the three-minute session needs refuge, refuge is grafted onto
warmth, and the landmark marks the end of warmth. So the card that said
*heaviness and warmth are yours* now adds that those two are exactly what the
short session needed, that it is on this screen already, and that the ladder
carries on alongside. A landmark that opens a door beats a pat on the back.

**The graft says what it is for.** Refuge arrives at warmth with no stated
purpose; it now ends with *once you move on from this step it is enough for a
short nidra session of your own*, which turns a drill into a countdown.

**The nidra card stopped reading like an ending.** *You have the entry, this is
somewhere to put it* was written when the card only appeared after the last
step. It now says to carry on up the ladder as well, that the induction here
grows as the sequence does, and that each longer session opens as its parts are
trained. The two tracks are meant to run together — that is what Phase 0 of
`PRIMED-NIDRA.md` describes — and until now the app implied you had to finish
one before starting the other.

Also spotted in the screenshot rather than the code: the regression note read
*"Warmth took you 4 days, and you are on day 0 of this one"*, because
`stepDays()` counts days practised and that is zero on the day you arrive.

### The expected order, stated everywhere and enforced in one place

Balance lets you start any programme without prerequisites, which is a fair
challenge to a screen full of locks. The answer turned out not to be *lock
everything* or *lock nothing* — the two tracks are not the same kind of thing.

**The autogenic ladder stays gated, and the gate is not a content lock.** It is
evidence that the response has arrived. You cannot skip warmth if warmth has
not turned up, and no button can grant it. Refusing to advance there is the
method; it is the one feature that makes this better than a syllabus.

**Nidra is only ever advised.** A session is content, and refusing to let an
adult open a twelve-minute recording is the wrong way to express a dependency.
The worst case is following instructions you have not trained — which is what
every nidra recording in the world asks of everyone. So the lengths open, and
each one says what it is made of that you do not have yet:

> This one uses sakshi, which you have not trained yet. It will still run — you
> will be following the instruction rather than issuing it, which is the
> difference the ladder is there to make.

The tile pill changed with it, from *needs* to **Usually after sakshi**, and
untrained lengths on the card are dimmed rather than disabled. Dimming is the
expected order; the tap still works.

So the order is now stated in four places and imposed in one:

- tiles are **numbered** within their track — 1, 2, 3 down each column;
- each track carries a caption saying what its order means. Autogenic: *in
  order, and held to it… that is evidence, not a lock.* Nidra: *runs alongside
  the ladder, from the first rung on… but none of it is locked;*
- every tile names what comes before it;
- the nidra card says the lengths are meant to be taken shortest first, and why
  — each one adds a stage the ladder trains.

**A locked tile is still tappable.** It cannot be practised early, but the
point of stating an order is that you can see what is in it, so a locked
autogenic tile now scopes the path below and lists its steps by name, each one
opening the existing preview. Reading is not advancing — the same principle
*Look ahead, but never advance* has always run on. Before this, tapping a
locked tile did nothing at all, which is the one interaction that teaches
nothing.

Two defects fell out of it. The nidra card was hidden behind `anyReady`, so
tapping a tile navigated to a card that was not there; it is now revealed by
being asked for, which keeps Practice one-thing-to-do on day one without
locking anything. And `check_app.py` caught a top-level `sx` — the onboarding
swipe's start-x — shadowed by the path's per-step `sx`; renamed `swX`.

### "wtf is refuge"

A nidra tile read **USUALLY AFTER SAKSHI** to a reader who had never met the
word, and the code was actively making it worse — `ndBlocker` split
`Pranamaya · counting down` on the separator and kept the half nobody could
read, throwing away the English gloss that was sitting right there. Two of the
six drills had no gloss at all.

And it was not confined to the tile. The same names are the **stage labels
shown during a session**, so mid-practice, eyes open, the screen said `SAKSHI`.

The app had already settled this once, for the three sankalpa modes, and the
comment in the source says why: they are *"named after what they actually are,
which is better writing as well as nobody else's vocabulary."* That rule was
applied to three buttons and nothing else. It applies everywhere now:

| was | is |
| --- | --- |
| Refuge | Somewhere safe |
| Pranamaya · counting down | Counting the breath |
| Opposites · heavy and light | Heavy and light |
| Opposites · cool and warm | Cool and warm |
| Sakshi | Resting as awareness |
| Sankalpa | The resolve |
| "At the sankalpa stages" | "When it asks you for something" |

The tile pill changed with them, from *Usually after* to **Easier after** —
smoother to read, states the benefit rather than a norm, and stays plainly
distinct from the ladder's *Opens after*, which is an actual lock.

Provenance is not lost, just not in the user's face: `PRIMED-NIDRA.md` keeps the
traditional names and carries the mapping.

### A programme is a screen

*Why not clicking a programme tile to full screen it and then show the path?*
It behaved like a full screen already \u2014 everything else hidden, a back row at
the top \u2014 but it was an in-place collapse, so the title bar said **Progress**
over content headed **The deeper four**, and an in-page heading repeated the
name underneath. The same duplication the nidra screen had before it moved out.

It is a screen now. The title bar names the programme, the count sits in the
slot the step counter uses because it answers the same question about whatever
you are looking at, and the in-page heading is gone. Progress stops mutating:
it always shows its three sections, with no hidden state behind it.

That surfaced a real defect in passing. The title bar had **two writers** \u2014
`go()` on navigation and `renderJourney()` on every re-render \u2014 so toggling a
step open on the path screen repainted the bar with the practice screen's name
and step number. One writer now, `paintTop()`, which reads whichever screen is
showing.

### Detail, high level, detail

Read back off the merged tab: *progress section, programme section, path
section \u2014 why? detail, high level, detail.* Correct, and the diagnosis
understates it, because two of those four sections were answering the same
question. The sequence already ends by naming the step after it \u2014 `NEXT \u00b7
BREATHING \u00b7 RIBS` \u2014 and the resting path said the same thing again as a rail:
where you are, and what is next.

The path only earns its place as a drill-in. It appears when you pick a
programme and it gets the screen to itself. What is left is three sections,
general to specific, with the log last:

| | |
| --- | --- |
| Your sequence | what you have \u2014 the payload |
| Programmes | what there is \u2014 the map |
| Turning up | have you shown up \u2014 the footnote |

Resting state went from 2.4 viewports to **1.6**. Nothing became unreachable:
revision and a step's briefing live in the path, which is one tap away on the
tile that is already outlined as the one you are in.

### Two tabs were both answering "how am I doing"

Observed, correctly: *practice and progress seem to be doing a lot of the same
thing \u2014 tracking. Programme is hidden in progress.* Four counters across two
screens:

| | |
| --- | --- |
| Practice | today's three slots \u00b7 `1 more day on this phrase` |
| Progress | `step 4 of 8` \u00b7 `6 of the last 7 days` |

The second half of the complaint was the worse one, and self-inflicted. One
commit earlier, shortening Progress, the programme tiles had been moved to a
screen of their own behind a text link at the bottom of it. That left a tab
holding a phrase stack, a week strip and a link, with the entire map of the
product hidden behind the link. Splitting it gave neither half enough to be a
screen and buried the half that mattered.

So it is one fault, not two: the second tab was split across two screens, one
thin and one hidden. They are one screen now \u2014 what you hold, whether you are
turning up, what exists, and the path through whichever part of it you pick.
Selecting a programme still collapses everything above it so the path gets the
screen, which keeps the deep state at 1.1 viewports while the resting state is
2.4.

The line between the two remaining tabs is **time**: Practice is today, and
this tab is everything longer than today. That is why the gate line stays on
Practice \u2014 *one more day on this phrase* is the answer to the practice you just
finished, and moving it here would restore the go-and-check behaviour it was
moved out of. And why the week strip and the ladder position stay here.

`step 4 of 8` went entirely. Position was stated three times on one screen: in
that counter, in the tile reading `IN PROGRESS`, and in the selected path's own
`0 of 4`. The track captions lost two lines each as well \u2014 they were written
before the tiles were numbered, and the numbers now say the order, leaving the
captions only the thing numbers cannot say, which is whether the order is
enforced.

**Still open, noticed while measuring rather than asked for:** the hero prints
today's three slots as their ratings \u2014 `3 / 3 / \u2013`. That is an outcome score on
the screen whose method says *do not try*, and `DESIGN.md` \u00a76 asks for the
opposite: rate the effort, treat less as better, and demote the landed
question. Onboarding is still five swipe screens of prose, and Learn is still
6,000 characters behind fourteen folds. All three are eyes-open surfaces that
have not had this argument applied to them.

### One thing per surface

Told twice that the screen still looked cluttered, and then: *if you could
start from a clean sheet, what would you do?* The first answer was a trim —
fewer words in the same boxes — and the reply was that it looked exactly the
same. It did.

**The timeline was the wrong metaphor.** A rail of dots with expandable rows,
a card nested inside a step inside a programme inside a screen, is the
course-app default, and it frames a method as a syllabus of things you owe.
The promise here is the opposite: it ends, and you keep something. What you
keep is the sequence you can say — and that sequence appeared exactly once, in
the lock-screen image, after nine weeks.

Progress is the sequence now. The run-through as you actually say it, in
serif, growing every time a step lands, with the framing line set quieter than
the formulae, the newest one marked, and the next named underneath. Below it
the week strip and one line — *6 of the last 7 days*. Below that, a link. No
cards, no rail, no pills, nothing to press.

**The gate moved to Practice.** *Can I move on?* is decided in one moment —
just after practising, when you rate it. Behind a tab it became something you
go and check, which is the behaviour a progress bar breeds. It sits under the
hero now, above the landmark card and the weekly question, because those are
an acknowledgement and a survey and this is the answer to what you just did.
The "ready to move on" nudge went with it: a card telling you to go to another
screen for something three inches below it is worse than no card.

**A gate with three conditions shows one.** The panel used to print all three
every day with a tick or a hollow circle against each — two of them things you
can do nothing about today, and on a fresh phrase all three unticked, which is
a report card issued before the term starts. The app already knew better: the
probe button is withheld until it is passable, because *a probe you cannot
pass yet is just a way of telling someone they are failing*. That was applied
to the button and not to the list above it. Now: the binding condition, the
one after it, and the whole rule folded into **How this opens**.

**Then the measurements.** Screenshots taken `full_page` make everything look
enormous, so: in viewports of 390×844, Progress and Programmes were 1.0–1.6
and Practice was **2.7**, of which 736px was the nidra card — a lede, four
lengths, a meta line, a warning, Begin, a fold, a second heading, three more
buttons and a text box. Length is the only choice anybody makes daily.
Everything set once went behind **Set up the session**, and then the card
itself went to its own screen, leaving one row on Practice reading *Primed
nidra · 12 min*. A second practice does not belong inline on the screen whose
job is to say what the one thing to do now is.

Programmes moved out the same way, and both lost the box they were drawn in:
a card border around a whole screen is the nesting the rest of the app had
just shed. Both keep the tab that owns them lit, since you got there by
tapping rather than by navigating.

| | before | after |
|---|---|---|
| Practice | 2.7 screens | 1.9 |
| Progress | 1.0 | 1.0 |
| Programmes | — | 1.6 |
| Primed nidra | — | 1.0 |

Three things that were said twice went as well: `STEP 2` in the title bar
beside `1 of 3` above a rail whose dot fill said it a third time; `DONE` /
`NOW` / `NEXT` pills against those dots; and the track name prefixing a
subtitle you reached from that track's own column. The `PROGRAMMES` heading
under a title bar reading Programmes, and the `N of 6 open` beside it, went
too.

One thing was tried and cut. Tapping a phrase in the stack to reach the step
that taught it needs a cue-to-step mapping that does not exist — warmth is
taught as *my right arm is warm* and appears in every later sequence as *my
arms are warm*, so half the lines opened the wrong exercise. Revision and the
briefings live on the map, where the steps are, and Progress stays the one
surface with nothing to press.

### Nidra was waiting for the whole ladder, for no reason

Asked what the quickest route from autogenic training to nidra is, by somebody
already feeling settled after heaviness and warmth. Two things were holding it
back and neither survived examination.

**The induction hard-coded all six exercises.** *My arms and legs are heavy and
warm. My heartbeat and breathing are calm and regular. My solar plexus is warm.
My forehead is cool.* So no nidra session could run until the last exercise was
learned — even though the induction's whole job is to make the state, and
heaviness and warmth make it for most people. It is now built from the sequence
you are actually practising and grows as you do.

**The card unlocked on `gate().done`.** But the three-minute session is settle,
induction, refuge, sankalpa and the cancellation — refuge is the only content
element in it, and refuge is grafted onto warmth. Somebody holding heaviness
and warmth has everything that session needs, and five more exercises was a
gate with nothing behind it.

Each length now opens when its own parts are trained: the field version and the
sleep version after refuge, the twelve-minute one once opposites, pranamaya and
sakshi are in. Locked lengths stay visible and say what opens them, since the
path is more use than a missing button.

The practical answer to the question: **three steps.** Heaviness in the arm,
heaviness in all four limbs, warmth — then a real three-minute nidra. At the
fast floor that is about twelve days rather than the eight weeks it was.

### A new phrase inherited the old one's day

Reported from real use: arriving on the second exercise, morning and midday
were already ticked with threes. They were — the ones from the phrase before.

`dayLog(today())` is every practice logged today whatever step it belonged to,
and the dose slots read straight from it. So advancing after a full day handed
the new phrase three completed slots, a *that is today's three* it had not
earned, and a next-practice pointer aimed at the sequence slot before the
phrase had been said once. The gate itself was never fooled — it counts
`e.step===S.step` — which is why this looked like a display quirk and was
actually the app telling somebody they had done work they had not done.

Log entries carry a timestamp, so the honest set is the practices logged since
you arrived on this phrase. Advancing now stamps `stepAt`, and the day's three
are counted from there.

It is worth saying this is the *ordinary* path, not an edge case: the gate
opens once the day's three are in, so almost everybody advances with a full day
behind them. Three more the same day is a lot to ask, so the new phrase says so
— you have already practised three times today, starting this one tomorrow is
perfectly fine, the count begins whenever you do — and the note goes as soon as
the first practice on the new phrase is logged.

### Two people felt it on the first listen

Reported from real use, which the app had no answer for. Every criterion in the
gate is about the response *not yet being there* — seven days, evidence it is
arriving, a probe. Someone in whom it arrives immediately rates three
unmistakable practices a day and is told *day 3 of 7*, which reads as the app
not listening.

The floor moves now. Four unbroken days where every single practice on the
phrase was immediate and unmistakable drops it from seven to four. Anything less
than all of that — one merely-clear rating, one missed day — and it is seven
again.

It does not go to zero, and the reason is worth stating rather than assuming.
Feeling heaviness on a first guided listen tells you the suggestion works,
which is a good sign and is not the same as having trained anything. A
recording told you your arm was heavy while you lay still with your eyes shut.
What is being trained is producing it yourself, in ninety seconds, sitting up,
on a bad day, with nothing playing — and the probe is the only criterion that
tests that, which is why it does not move at all.

The recency requirement was not in the first version and the tests caught it: a
day three weeks ago plus a strong return counted as four days on the phrase, so
the fast floor let a lapse through the gate the slow floor had just been fixed
to hold. It now asks for the last four days specifically.

Learn gains *It happened on the first try*, which until now had no entry — the
whole of "if it feels wrong" addressed people who felt nothing.

### Explaining and guiding are not the same pace

The films were all rendering at ElevenLabs' 1.0, which is that voice's natural
cadence: measured, unhurried, right for walking somebody into a relaxation
exercise and wrong for telling them a fact. Reported as too slow, and it was.

The distinction is what the recording is *doing*. A practice track paces your
breathing; a briefing is somebody explaining something. So the seven
explanatory films — after-first, finished and the five exercise briefings — now
render at 1.1, and the practice recordings stay at 0.96 where they belong.
Roughly ten percent off each, and *after your first practice* comes down from
1m 44s to 1m 33s.

Not touched: the pauses. Nine seconds of silence across a hundred-second film
is not what makes it feel slow, and those pauses are where a slide change
lands.

Auditing that turned up a quieter inconsistency. Six of the seven practice
recordings carried no render directive at all and were taking the tool's
default, while the newest named 0.96 — so the one recorded last was faster than
the six it shares a sequence with, for no reason anybody chose. Every script
states its pace now, and `check_app.py` enforces the rule: a script the ladder
plays renders at 0.90, everything else at 1.1. Verified by flipping a briefing
to practice pace and watching the build refuse it.

All seven audio tracks and all seven films re-rendered, posters regenerated in
the same pass so they cannot drift from the video they came from.

### Both halves now have the same shape

Slide three's list worked, so slide two got the same treatment — and it had the
same defect for the same reason. *Less noise in your head. Coming down faster
after something stressful. Getting to sleep.* was three list items trailing off
the end of a paragraph about something else, which is where a reader stops
noticing them.

Both screens are now **lead, list, caveat**. Slide two: what you do, what the
heaviness means, what people notice, then the hinge into the next screen. Slide
three: how many are coming, the three of them, then why a recording cannot
teach them. The parallel is worth having beyond tidiness — the two halves of
the product are meant to be counterparts, and reading identically is the
cheapest way to say so.

Slide two lost about fifteen words on the way: *"you notice it happen"* after
"the arm does feel heavy" was saying the same thing twice, and *"there are
eight in all, one at a time"* moved into the caveat where the other
housekeeping lives.

### The three things were a list pretending to be a paragraph

Slide three ran to 137 words in three paragraphs, the last of them five lines
deep. The bulk of it was that the three practices — the resolve, the opposites,
the sitting still — were being read out as prose when they are plainly a list,
and a reader has to hold all three in their head to see there are three.

They are a list now, in the same bulleted style the benefits use, and the
opener says how many are coming before they arrive. 97 words on screen, down
from 137, with no idea removed.

The recording explanation went into the quieter caveat style, which is the
right register for it: it is the reason behind the screen rather than one of
the three things on it. It also lost the closing clause about issuing the
instructions being possible only because you can make the state — true, and
already said twice on this screen and the one before.

### Tighter, minus three regressions

A tightening pass came back with real improvements and a few things that undid
the last two fixes. Taken: **The state is the foundation** as slide three's
opener, which is a better sentence than the one it replaced; shorter clauses
throughout; and dropping the trailing *instead of lying there running the day
back*, which the sleep line did not need.

Not taken, and worth naming:

*Repeat a short phrase **like** "my right arm is heavy"* reintroduces the
example ambiguity fixed one commit earlier — it is not like the phrase, it is
the phrase, and *there are eight in all* went with it.

*It's **proof** you've entered the state.* Heaviness is a sign, not proof.
Peripheral warmth and muscle tone are correlates of the shift, and calling a
correlate proof is the kind of sentence a claims review removes. Sign is both
safer and more accurate.

*It works, and you don't even have to try.* Two problems: it is a bare efficacy
claim, and it replaced the hinge — *it has nothing at all for you to do once
you are there* — which is the line that sets up the entire next screen.

And the flagged one was right. *Recordings can't replace it* asserts the
conclusion and drops the reason. A recording keeps going whether or not you are
still awake, so you recognise the instructions instead of issuing them, and
recognising is not learning. That is the argument for the whole product, and it
now sits on the screen rather than being alluded to.

### "One short phrase" needed to say which one

*You repeat one short phrase to yourself — my right arm is heavy — and after a
few days the arm actually does feel heavy.* The dashes make it read as an
example drawn from a set nobody has described, which raises the question it was
meant to answer: one phrase out of what?

It is not an example. It is the phrase they will be handed about a minute
later, and the ladder is eight of them. So: *You repeat one short phrase to
yourself. The first is my right arm is heavy… There are eight in all, one at a
time.* Same length, and it previews the thing rather than gesturing at it —
someone arriving on the practice screen now recognises the sentence.

It also quietly does a job screen four was doing alone: the ladder has a size,
and knowing it is eight before agreeing to start is fairer than finding out
afterwards.

### The two halves were not joined

Slide three opened on *"the state you have just made"* — and slide two had
never said there was a state. It described a phrase and a heavy arm, then ended
on "getting you somewhere" and "once you arrive", both of which are the
narrator knowing something the reader has not been told.

The missing link was already written, in the film shown after the first
practice: heaviness is not the goal, it is the *signal* that the body has
dropped out of alert mode. Which is exactly the sentence that makes the rest of
the product make sense, and it was being withheld until after somebody's first
attempt.

Slide two now says it, in the middle where the benefits used to start cold:
the heaviness is not the point, it is the sign the body has shifted, and that
settled state — reached on purpose in about ninety seconds — is the thing being
trained. The benefits follow it as consequences rather than as a list, and the
closing line changed from "getting you somewhere" to "getting you into that
state".

Slide three then reads *three things, and every one of them needs that state
first — which is why nobody can teach you these on their own*, which is both
the join and the argument for the whole product, in one sentence.

Neither screen grew: both are still 733px, because the words that were doing no
work paid for the ones that were.

### Reading the introduction back, three cuts

**Slide one lost its caveat.** *"You will be taught one thing at a time, in
order, and never the second before the first can carry it"* is reassurance
about pacing, offered before anyone knows what the pacing is of. The headline
and one paragraph say what the thing is; that was the screen's whole job.

**The mechanism moved to slide two and out of slide four.** *You repeat one
short phrase — my right arm is heavy — and after a few days the arm actually
does feel heavy* was sitting on the dose screen, describing the first half a
screen and a half after the first half had been described. It belongs in *The
way in*, and slide four is about ninety seconds and three times a day.

**Slide three was insider vocabulary.** "A resolve held as though already
true", "opposite sensations invited and let go", "resting as the awareness that
was there the whole time" — every phrase in it presumed the reader already knew
the practice being described. It says what you actually do now: you say one
sentence about how you mean to be as though it were already so, you call up a
feeling and then its opposite — heavy, then light, which is the exercise they
are about to start — and you spend a few minutes with nothing to do at all,
which is harder than it sounds.

That last change matters most. Naming the opposites pair as *heavy, then light*
ties the abstract half to the concrete one on the previous screen, and it is
the actual first opposites drill they will meet at step four.

### Give each half its own screen, and drop the benefits

The two-halves explanation was three paragraphs stacked on one screen — the
most distinctive thing the product has to say, crammed — while a whole screen
went to four soft benefit bullets we had deliberately kept vague for claims
reasons. The real estate was allocated backwards.

Each method has its own screen now. **The way in** and **Somewhere to go**,
titled with what each contributes rather than with its name, since the headline
before them has already given both names. And *Somewhere to go* finally says
what nidra actually contains — a resolve held as though already true, opposite
sensations invited and let go, resting as the awareness that was there the whole
time — which the app had never stated anywhere on the way in.

The benefits screen is gone. They survive as a clause inside *The way in*,
which is where they belong: less noise in your head, coming down faster,
getting to sleep, said in passing while describing what does it, rather than as
a list of promises on a screen of their own. Learn keeps the fuller version.

Five screens, none over 735px, all navigable both ways.

### Four screens, and a way back through them

The introduction had been squeezed to two screens on the way to cutting
clutter, which made the first one carry the mechanism, four benefits, the dose,
the fade and a caveat — 855px of one screen doing four jobs. Splitting it back
out gives each screen a single thing to say: **what this is**, **what people
notice**, **what it asks**, and the cautions. Nothing over 735px, and the
benefits got their explanatory sub-clauses back, since there is room again.

The part that makes four screens work rather than merely tolerable is being
able to go back. A row of dots you cannot return through is a slideshow, not
something you can read at your own pace — so there is a Back button from the
second screen on, the dots are tappable, arrow keys work, and swipe goes both
ways.

The swipe has the check that matters: a gesture is only a page turn if the
horizontal distance beats the vertical by half again. These screens are taller
than a phone, scrolling them is the commonest thing anyone will do here, and a
scroll misread as a page turn would be worse than no swipe at all. Verified by
dispatching a steep drag and confirming the screen does not change.

### The introduction never said what it was

It opened on a benefit — *an off switch you can reach for* — listed four more,
gave the dose, and explained the fade to nothing. Why and how, and no what. The
closest it came was a caveat at the bottom saying what it is *not*: not a mood,
nothing to believe in, nothing to concentrate on, and here is a German name for
it.

The what had only ever been said in the film — *"you repeat one short phrase to
yourself, my right arm is heavy, and after a few days the arm actually does
feel heavy"* — so deleting the film took it out of the product entirely. Nobody
noticed for one commit, which is the interesting part: the pitch reads fine
without it, right up until you ask what the thing actually is.

It leads on the mechanism now, before any benefit: one phrase, a few days, the
arm feels heavy, you notice it happen. The four benefits lost their explanatory
sub-clauses to pay for it, which they could afford — *"Getting to sleep"* did
not need a second sentence about lying there running the day back.

The caveat also stopped pretending there is one method. It names autogenic
training, says a second one joins at the third step and that it is what the
state is *for*, and points at Learn. Someone reaching the warmth step and
finding Refuge grafted onto their practice has now been told twice that it was
coming.

### The intro film is gone

Demoted to Learn in the morning and deleted by the afternoon, for a reason the
demotion did not fix: it described autogenic training and nothing else. That
stopped being the product two methods ago. A film that opens *"there are six
exercises"* and never mentions the second half is not merely thin, it is
wrong — and keeping it in Learn only meant the wrong version was one tap away
instead of unavoidable.

It was also the single largest maintenance burden in the repository. Every
content change meant re-rendering two minutes of narration and eighteen slides
to keep it honest, four times in one day, and it fell out of date between the
render and the commit more than once. What it explained now lives under Learn,
where a correction is a sentence rather than a build.

Deleted with it: `script/intro.md`, `audio/intro.mp3`, `video/intro.mp4`, its
poster, its slides and its timings — and the path row that replayed it, the
`AUDIO.intro` keys, and `obStopVideo()`, which had nothing left to pause. The
built site went from 13.1 MB to 10.9 MB.

If an overview film is ever worth making again, it has to describe both methods
and the graft between them, and it should be made once the shape has stopped
moving.

### How it got there: the intro film left the critical path

Asked whether onboarding needed the cards *and* a film, and then whether the
film earned its place at all. Laid side by side the answer was not close: the
first two screens were the film's own script, in text, immediately before the
film. *Less noise in the head — not silence, the volume down* is on screen one
and in the narration, word for word. So is *ninety seconds, three times a day*.
So is *you end up not needing this*.

And the film is not animation, whatever the effort in it. It is eighteen
typographic cards with a synthetic voice reading alongside them — which is
slower than reading and thinner than watching. Two minutes and fifteen seconds
of being told about something you could have spent ninety seconds doing.

This decision had already been made once. The six-minute explainer was deleted
months of commits ago and replaced with just-in-time briefings, on the argument
that nobody has the questions before they have the experience. The intro film
was the last survivor of the explain-first era and nobody had applied the
lesson to it.

Onboarding is two screens now — what this is, and the cautions — with the dose
strip and *and then you stop needing it* folded up from the deleted screen, so
nothing is lost. The film moved to Learn under *The two-minute introduction*,
where somebody who wants the overview can have it and nobody is made to sit
through it first.

Day one is now: one screen, the cautions, the contrast drill, and a practice.
The drill is forty-three seconds and produces the sensation the whole method is
aimed at, which is a better use of a first minute than a narrated summary.

### The practice screen had grown a queue

Reported as cluttered, and measured before touching it: on a step change with a
week's question due, the practice screen ran to 1,020px and **Start practice
was below the fold**. Four separate cards had claimed the position above the
hero — the day-one drill, the welcome back, the halfway landmark and the weekly
question — and any two of them together buried the button you open the app to
press.

Only one card may sit there now, and only if it changes what you are about to
practise: the drill offer and the return from a lapse qualify, an
acknowledgement and a survey do not. Those two moved below the hero.

Three redundancies went with it. The sound key was three lines explaining four
notes on the screen you open six times a day — one line now, the full version
in Learn. The graft block was six elements for a forty-second addendum; the cue
appears during the practice where it is needed, so the card names it, says how
long, and puts the rest behind *What to do*. And *"Today's review is heaviness
· right arm"* was the third place on one screen saying the same thing, after
the slot labelled REVIEW and a button reading *Start review — heaviness*.

An ordinary week is 715px with Start fully visible; day one is 496px.

### Two landmarks were pinned to step numbers

Found while measuring the clutter, not by looking for it. The halfway card
fired on `S.step===5` and the discharge reminder on `S.step===7||S.step===8`,
both written against the ten-step ladder. After two cuts that put the halfway
mark at the warm centre — three steps late — and the discharge reminder past
the end of the ladder, where it could never fire at all.

They read the ladder now: halfway is the step after the last Warmth step,
and the deep ones are whichever steps are called Warm centre and Cool head. A
number that means "the step after warmth" should never have been written as 5.

### Nowhere did the app say it was two methods

The grafts shipped without a word of explanation. Somebody on the warmth step
would have found a Sanskrit noun appended to their autogenic practice, for no
stated reason, from an app whose entire pitch had been six formulae. The intro
film is pure AT, Learn covered doing it right and what to do when it feels
wrong, and the fusion — the actual thesis — appeared nowhere a user could
reach.

Learn now has **Why there are two methods here**: autogenic training is very
good at getting you somewhere and has nothing for you to do once you arrive,
since all six exercises are ways *in*; nidra is almost all content and has no
way to teach any of it, arriving as a recording that carries on whether or not
you are still awake. Each supplies what the other lacks.

That section also answers the question the design raises, which is why the
nidra elements hang off the end of a practice instead of being practised on
their own: **they need the state the formula has just produced.** Refuge
entered cold is a different and much harder exercise, and it is the one that
does not stick. That is the whole of "primed" in Primed Nidra, and it had never
been said outside a markdown file.

The first graft carries a short version of it plus a link into that section,
and later grafts do not repeat it.

### Nidra's elements get trained the way the formulae do

The thesis of `PRIMED-NIDRA.md` is that autogenic training has a pedagogy and
nidra has none. Until now the app only demonstrated half of that: the ladder
trained its formulae properly and then dropped the nidra elements in whole, at
minute four of a twelve-minute session, exactly the way every nidra recording
does.

They are now **grafts** — forty seconds appended to a practice, not a second
practice. Each sits on the formula sharing its substrate: refuge is entered
through warmth and contact, so it lands on the warmth step; counting breaths
lands on the breath. Two of the day's three carry it and the review stays pure
AT, which is the protocol's own ratio, and a guided session never does, because
the recording has no room and the graft is self-issued anyway.

Wording is fixed and shrinks on days carried, by the same mechanism as the
formulae — *"Let heaviness fill the arms. Now release it and find lightness.
Now both at once."* → *"Heavy… light… both."* → *"Both."*

**Sakshi is deliberately not drilled**, and neither is the sankalpa. The
document is explicit: they are defined by the absence of a doing, so training
them toward automaticity would condition a manoeuvre where the point is that no
manoeuvre occurs. They get time, not repetitions, and the card says so instead
of showing a criterion.

Criteria for the rest are stated and not gated. The ladder already paces
progression; a second gate on a self-reported ten seconds would be a scaffold
pretending to be a ruler.

A third chime marks the formula ending and the graft beginning, since two
thirds of the practice is now eyes-closed with something changing partway.

One trap worth recording: a test seeded a record without a version stamp, so
the migration correctly walked its step down two ladders and the graft looked
broken. The app was right and the fixture was wrong — seeds need `v` now.

### Look ahead stopped at the end of the ladder

It listed every step and nothing after them, so the half of the programme that
is not autogenic training — the stages, the sankalpa, the opposites — could be
*run* but never *read*. Twelve minutes is a long way to go to find out what
something is made of, and the stage table was sitting in `nidraStages()` the
whole time.

The nidra card now carries **What is in it**: every stage of the selected
length with its duration and its cue, generated from the same function the
runner uses, so it cannot describe a session the app does not deliver. All
three lengths, including the sleep variant's open-ended third stage, which
shows a dash rather than a time because it has no end. Underneath, the nine
opposites pairs and the note that they rotate one per session.

Look ahead also gains a final row — *After the ladder · primed nidra* — which
enters the finished state and scrolls to the card. That was reachable before
only by knowing that the last step, a week in, is where the door appears, which
is not something anyone should have to know.

### The introduction was the one thing you could not go back to

Reported as "I don't see the changes" after the first screen was rewritten, on
a device confirmed to be running the new build. Both were true. The four
onboarding screens are shown by `if(!S.onboarded) obOpen()` and from the reset
handler, and from nowhere else — so once you have onboarded, that copy is
unreachable no matter how many times it is rewritten.

Which makes it the only content in the app you could not get back to. The films
replay from the path, the contrast drill sits in Learn, briefings stay findable
after they are watched — that principle is written down in this README, and the
screens that set the whole thing up were the exception nobody noticed.

Learn now has *The introduction, again*. Replaying returns you to the screen
you asked from rather than dumping you on Practice, and touches no state: a
record part-way through the ladder comes back with its step, its log and its
onboarded flag exactly as they were.

Worth naming the diagnostic failure too. The first three explanations offered
were a failed deploy, a stale service worker and a cached install — all
plausible, all checkable, all wrong, and two of them cost a build stamp fix to
rule out. The actual cause was that the screen renders once in the app's
lifetime. "It is not deployed" and "you cannot get there" look identical from
the outside, and only one of them was worth checking first.

### Not leading with somebody else's category

The first screen and the first film both opened on *if meditation never stuck*.
It is an efficient hook — five words that tell you this is not what you assume
and that it asks less. It also has to go.

**The product now ends in yoga nidra, which is meditation.** Not concentration
meditation, and not seated attention training, but a meditative practice by any
ordinary use of the word. Opening with "meditation didn't work for you" and
closing with a twelve-minute nidra session is a contradiction anyone who gets
there will notice, and they will be right.

Two more reasons, both true before nidra was in. Negative positioning defines
the thing by what it is not, and hands its category to the competitor in the
first line. And it addresses a failure state, so everyone who never tried
meditation is excluded by the opening words.

The screen leads on **a response you train**, and the film on *there is a
settled state your body reaches on its own, usually when you are not looking —
this is how you learn to reach it deliberately*. Its first slide said
"Autogenic training." — the jargon problem again, in the film this time — and
now says what that means.

What is worth keeping from the meditation frame is true of both halves and
belongs at the end rather than the front: neither AT nor nidra asks for
sustained concentration, which is the thing people actually fail at. That is a
better claim than "not meditation", and it is only credible once someone has
felt it.

The benefits list stays as it is. It is all switching *off* — quieter head,
coming down faster, sleep — which is honestly what the first eight steps
deliver. The switching *on* half is the sankalpa, it has the least evidence
behind it, and it arrives when it becomes real.

### A full content pass after the ladder changed

Cutting heaviness twice left copy pointing at a shape that no longer existed.
A sweep of every script, slide and screen turned up six kinds of drift, and
only two of them needed audio.

**Spoken step numbers, again.** The last pass stripped them from the *opening*
of six recordings and missed the *closing* line of five — "That's step five.
Ninety seconds, three times a day, on your own." Half a fix reads exactly like
a whole one when you only grep the thing you remember writing. Every script is
now silent about its position: the screen says which step you are on and the
recordings never contradict it.

**The intro enumerated the old ladder.** "Heaviness in the arms. Then
warmth" — spoken, and the ladder slide agreed with it. Both name arms and legs
now, which is what the single heaviness formula actually says.

**The intro denied its own gate.** "You move on when your own record says it is
landing — not when a week has passed" was wrong in two directions: a week is
required, and there is a probe as well. It now says landing *and* unaided, with
a week as the least it takes rather than the whole of it.

**Five scripts stated the old criteria** in prose — "at least five days
regardless" against a seven-day floor and an unguided probe. Prose, so no
re-render.

**Five briefings named a step number** in their headers, from a ladder two
edits ago. They say "when you reach it" now.

**Onboarding hard-coded "10 steps."** It reads `STEPS.length`, because that
number has now been wrong twice.

Also swept out: two cue-shrink entries for formulae no step speaks any more,
and dead audio keys in the fallback map.

### Heaviness lost a week, and the recordings stopped counting

Four heaviness steps — right arm, left arm, both arms, legs — was four weeks
for something the body largely does by transfer, and it went to two in two
goes. The dominant arm keeps a step of its own: that is where the response is
learned against never having felt it, and where nothing may happen for a
fortnight. Everything after it is the classical formula, *my arms and legs are
heavy*, naming all four limbs at once.

The three intermediate stops were spent proving something that happens anyway.
The response is learned once; after that it is being named somewhere else,
not learned again. Time-to-warmth — the first unmistakable sensation — goes
from four weeks to two, and the ladder is eight steps.

The objection to two turned out to be about a recording rather than a
principle: merging the legs in *looked* like changing the phrase mid-step,
because the legs track was written as "arms first, now legs". Rewritten as one
formula, with the arm you already have as an anchor said once at the start,
nothing changes mid-step.

The blocker was that six recordings opened by announcing their own position —
"Step seven. Heaviness, warmth, heartbeat, then the breath" — so any change to
the ladder desynchronised the narration from the screen. That had already
shipped once, when inserting the legs left five recordings saying a number one
lower than the app displayed. The numbers are simply gone now; the screen says
which step you are on, and the recordings never contradict it again because
they no longer have an opinion. Six re-renders, cheap because the segment cache
only missed the lines that actually changed.

A stored record still points at the old indices, and silently — the numbers
resolve, they just mean a different exercise. So `migrate()` remaps step, log,
`probed` and `skipped` once, writes the result back, and stamps `v`. Both old
both-arms steps land on the surviving one.

Two bugs in writing it, the same shape twice: a `const` referenced by a hoisted
function that runs before the declaration is evaluated. `load()` is called
above where it is defined, so `STEPS` and then `LADDER_V` were both in their
temporal dead zone, and each one threw at boot and took the entire script with
it. `check_app.py` passed on both, because the file parses perfectly either
way. `test_journey.py` now boots a pre-v2 record and asserts no page errors,
which is the only thing that would have caught either.

### The gear was a sun

The header button had `class="gear"`, `aria-label="Settings"` and a `data-go`
pointing at the settings screen — and drew a circle with eight radiating lines,
which is a sun. On a phone a sun means one thing: switch to light mode. So the
one control that opened Settings was advertising a theme toggle, and this
README had been calling it a gear for days on the strength of the class name.

Almost certainly a fossil: Settings began life as the theme control, where a
sun was apt, and grew into a screen without the icon following. It draws a gear
now.

Worth noting how it survived. `check_app.py` verifies that every `$('#id')`
resolves and every on-screen cue is spoken; nothing it does could ever look at
a path and see the wrong picture. Neither could `test_journey.py`, which clicks
the button and lands on Settings exactly as intended. This one needed eyes, and
it took a user's.

### Settings is not a tab; nidra was in the wrong room

Asked whether Settings should be promoted to a fourth tab, on the reasonable
grounds that it had grown a lot. The growth was the symptom.

Settings was created behind a gear on the principle that the tab bar is for
things you do, and preferences are not one of them. That principle still holds.
What had happened is that a whole second practice — a twelve-minute nidra
session and the sankalpa it is aimed at — had been filed in the preferences
drawer, where it was both mis-shelved and effectively unfindable. The commit
that put it there said Settings is where features go when nobody has decided
what they are, and then left it there, which was the tell.

`DESIGN.md` §8 already said where it goes: nidra is the door at the end. So the
card now sits on Practice, below the hero, appearing when the ladder is
finished — which is exactly when the Practice screen has the least to say and a
"what now" belongs. Its copy changed with its address, from an apology for
being in Settings to the thing it is: *you have the entry, this is somewhere to
put it.* A finished session returns there rather than to Settings.

Settings is back to four preference cards — appearance, look ahead, reminders,
your record — which is a gear's worth of screen.

### The three sankalpa modes are named for what they are

They were *Simplify being*, *Enquiry* and *Embodied* — a triad lifted from a
modern author's framework. They are now **Presence**, **Question** and
**Resolve**, which is what each one actually does: the slot held open with
nothing asked for, a question asked once and listened to, or a fixed statement
held as already true.

Worth separating the two things tangled together here. Short names and labels
are not protected by copyright, and a *method* is explicitly excluded from it —
this is a trademark-and-attribution question, and a mild one. The Sanskrit is a
separate matter again and carries no risk at all: *sankalpa*, *pranamaya*,
*sakshi* are traditional terms centuries older than anyone's book, and they
stay.

But the borrowed triad was worth losing regardless, because it was also the
worse writing. *Simplify being* tells a first-time reader nothing, and
*Embodied* is jargon standing where a plain noun belongs.

Old records carry the old keys, so `ndState()` maps them forward on read.

### The look-ahead could not see the ending

Preview marked no step as probed, so `gate().ready` and `gate().done` were
false at every step it could show. It let you look ahead at every step's
practice and none of the moments that decide anything: the gate unlocking, the
Finished screen, the sequence-as-an-image offer, and the nidra door behind it.
The last screen in the programme was the one screen preview could not reach —
and that is where the sankalpa lives.

"A week in" now means the gate is genuinely open, which is what someone looking
ahead is looking for. "Just arrived" still shows the criteria unmet, because
that is the honest day-one view.

So the sankalpa is reachable today without waiting ten weeks for it: Settings →
Look ahead → step 10 → a week in. Nothing written in there is saved, which is
the point of preview and also the limitation — a resolve set in preview is a
rehearsal, not the real one.

### No splash screen, but no flash either

Asked whether the app should open on a screen saying *Switch*. It should not,
and the question was worth asking anyway because something at launch did look
unfinished.

Against a splash: an installed PWA already gets one, generated by the browser
from the manifest's name, icon and background colour, so a second would show
the name twice in a row. And this is a product used for ninety seconds, three
times a day — a second of branding on each launch is six seconds a day against
four and a half minutes of practice, spent asserting a brand at someone whose
app has spent every other screen promising to get out of the way.

What actually looked wrong were two flashes, both from decisions taken in the
main script — which runs *after* the page has been painted once.

**The theme.** Anyone who had overridden their phone's setting got a flash of
the other palette on every launch, and the status-bar colour was hard-coded
dark, so light-mode users got a dark bar corrected a moment later.

**First run.** A brand new install painted the empty frame of an app it had not
been introduced to yet — header, tab bar, hollow card — and then dropped
onboarding over the top.

Both now settle in a blocking inline script in `<head>`, before the first
pixel: read the stored record, stamp `data-theme` and the real status-bar
colour, and on a first run mark the document so the frame stays hidden until
onboarding is up. Wrapped in a try, so a browser that throws on `localStorage`
in private mode falls through to the defaults rather than taking the page down.

Verified across all four theme combinations, and the first-run class caught in
the act by hooking `DOMTokenList.remove` — set before the app boots on a clean
install, never set for a returning user.

### It is called Switch

The tab, the bookmark and the home screen said *Autogenic Training* and
*Autogenics*. Nobody arrives knowing the term and nobody searches for it, and
naming the product after the method had become wrong in a second way: the
method is no longer the whole product. Yoga nidra is in here too, and a name
that covers one half misdescribes the thing.

Switch covers both, and in both directions — off, which is the ladder and the
trained relaxation response, and on, which is the sankalpa and whatever it is
aimed at. It is one word, six letters, legible as an icon label, and it names a
capacity rather than an outcome, which keeps it clear of the claims line that
*Change* and *Mind Strengthening* both crossed. It is also already the
approved headline: *an off switch you can reach for.*

The first screen still supplies the off-reading immediately, so the name is
legible on day one and grows an extra meaning when nidra arrives at the end.

One honest cost: as a search term it belongs to a games console. Irrelevant for
a personal install, and it would matter on a store listing.

`autogenics` stays as the repository and Pages URL. Renaming those would break
every installed copy for the sake of tidiness.

### Pull-to-refresh, off

Scrolling a list with a thumb ends at the top of the page as often as not, and
one more millimetre there reloads the app. Reported as an annoyance; it is
worse than that. A reload during a practice destroys the session outright —
the timer, the pre-scheduled chimes and the take-back all live in memory, and
the take-back is the part the cautions call non-optional.

`overscroll-behavior-y: contain` on the root turns the gesture off, and the
full-screen overlays get `overscroll-behavior: contain` too so a swipe on a
practice screen cannot chain out to the page behind it. Nothing here needs
refreshing by hand: the service worker updates itself, and now defers the
reload while a practice is running.

### A tab bar of double height

Reported from Android Firefox: the bottom nav sometimes drew at twice its
height, with an empty band under the labels.

`viewport-fit=cover` plus `padding-bottom: env(safe-area-inset-bottom)` is the
standard way to keep a fixed bottom bar clear of a home indicator, and it
assumes the page is what reaches the bottom of the screen. In a browser tab it
is not — the browser has already reserved the system navigation bar, and then
reports the inset as well. So the padding was added on top of space that had
already been taken, and the band underneath was exactly one system-bar tall.

The inset is only ours to add when the page really does own the bottom of the
screen, which is when it is installed:

```css
:root{--safeb:0px}
@media (display-mode:standalone),(display-mode:fullscreen),(display-mode:minimal-ui){
  :root{--safeb:env(safe-area-inset-bottom,0px)}
}
```

All four places that reserved bottom space now use `--safeb`. In a tab the nav
measures its content height and sits flush with the viewport; told to behave as
though installed with a 48px inset, it grows by exactly 48px and no more.

The trigger turned out to be more specific than "sometimes": scroll to the
bottom with a thumb and the bar is fine, touch the screen again and it doubles.
That is Android Firefox's dynamic address bar sliding back in. Two more changes
so the layout cannot care what it does:

`min-height:100dvh` in place of `100vh`, because `vh` is frozen at the *largest*
viewport — the one with the address bar hidden — so on its return the layout is
sized for a window that is no longer on screen. `dvh` tracks it, with `vh` left
in front as the fallback.

And the nav is `box-sizing:border-box; overflow:hidden`, so whatever any of this
reports, the bar is its contents plus whatever inset is genuinely ours and
cannot render as anything else.

Measured through a simulated address-bar cycle — 844px, 760px, back to 844px —
the nav stays 63px and flush with the bottom at every step, and still grows by
exactly 48 when told to behave as an installed app with a 48px inset.

### The recorded-voice feature, and why it is gone

Built, shipped, and removed the same day. Recording the formulae in your own
voice sounds like it serves this method — it is autogenic in the literal sense
— and it fails the product's one real test.

The app's whole claim is that you stop needing it. A set of your own recordings
is a personal library: an artefact that makes the app more yours and leaving it
more expensive. `DESIGN.md` §6 forbids a library for exactly that reason, and
§1 says every standard engagement mechanic is harmful here. It was a retention
mechanic, built by the same person who wrote the section forbidding them.

The diagnosis was wrong too. The problem was "eyes shut, a line on screen
reaches nobody" — which is true and does not argue for audio. Someone in timer
mode is *supposed* to be issuing the phrase to themselves; that is the
practice, not a gap in it. And a nicer voice is a stickier scaffold: guided →
timer → nothing works partly because a stranger's pacing is mild friction, and
friction is what gets people to drop it on schedule.

Kept in `DESIGN.md` as a withdrawn section rather than deleted, so it does not
get reinvented in three months.

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
