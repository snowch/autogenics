# If we built it again

Written after building the thing once, reading the literature, and watching
where it creaks. This is an argument, not a backlog. It contradicts some of
what is already shipped, which is the point of writing it down.

---

## 1. What kind of product this actually is

It is not a meditation app. The comparison set people reach for — Calm,
Headspace, Insight Timer — is a **content** business: a library, a
subscription, a reason to open it again tomorrow forever. Every UX convention
those products use is tuned to retention.

This is a **motor-skill training programme**. Its closest relatives are
physiotherapy-adherence apps, Duolingo, and 1970s biofeedback trainers. The
deliverable is a conditioned response the user keeps after uninstalling. The
business model implied by the method is the opposite of a subscription, and
pretending otherwise is what would make it mediocre.

Three consequences follow, and almost everything else in this document is
downstream of them.

**The whole game is the first ten days.** Days 1–10 are the period when you
practise faithfully and feel nothing. That is where people quit. Content,
polish, and breadth of features do nothing for this. Only evidence does.

**It is used with the eyes shut.** Ninety seconds of the interaction is
eyes-closed; twenty seconds either side is not. So the craft that matters is
audio, haptics and timing — not screens. We have been designing the wrong
surface beautifully.

**Every standard engagement mechanic is actively harmful here.** The single
instruction of the method is *do not try*. Streaks, goals, scores and progress
bars all manufacture trying. This is a rare product where the growth playbook
and the method are in direct opposition, and the method has to win.

---

## 2. The one bet: close the evidence gap

If I could change one thing, this is it.

Right now the app asks the user whether it landed and takes their word for it.
That is noisy, it is unverifiable, and worst of all it makes the user the
judge — which invites exactly the self-monitoring effort that blocks the
response.

**Measure something real, and show it afterwards.**

What a phone can honestly do: camera-plus-flash PPG on a fingertip gives a
reliable pulse rate, and a usable — not clinical — beat-to-beat series. Across
ninety seconds, pulse rate change is the defensible number. HRV from ninety
seconds of phone PPG is marginal and I would not build a claim on it.

What a phone cannot do: skin temperature. Peripheral warming is the
best-established physiological correlate in this method's own literature, and
it needs hardware — a wearable, or a cheap thermistor. If this product ever
justifies an accessory, a £4 fingertip thermistor is the one.

Three rules make it help rather than hurt:

1. **Never during.** A live readout turns the practice into a performance and
   defeats the thing being trained. Capture silently, reveal after.
2. **Report, do not score.** "Your pulse settled by 6 across that ninety
   seconds" — an observation about the body, not a mark out of ten. No target,
   no green tick, no comparison to yesterday's best.
3. **Say nothing when there is nothing.** Days with no change get "no change
   today", stated as unremarkable, because it is.

The strategic value is not the measurement. It is that day 3 stops being an
act of faith. That is the difference between a product with a 12% completion
rate and one with a 40% completion rate, and no amount of interface craft
substitutes for it.

**Caution, stated plainly:** measuring physiology and displaying it moves the
product closer to the regulated end of the spectrum in several jurisdictions.
The framing has to stay descriptive — what the body did — with no inference
about health, and legal review before it ships. That is a real constraint on
this idea and I would not pretend otherwise.

---

## 3. Make the first session produce a sensation, not an explanation

Today, day one is: watch a two-minute film that *explains* heaviness, then go
and repeat a phrase and feel nothing. We are asking someone to aim at a target
they have never seen.

Invert it. The first ninety seconds should **induce the referent**, physically,
in the room, on the first try. Two candidates, both reliable:

- **Contrast.** Clench the right fist hard for ten seconds. Release. The
  twenty seconds after release is heaviness — unmistakable, in everybody, first
  time. Then: *that is what the phrase points at. You are learning to get there
  without the clench.*
- **Passive weight.** Let someone else, or gravity, take the arm's weight and
  drop it. The felt difference between a held and an unheld limb is the same
  signal.

This costs nothing, needs no hardware, and converts the abstract noun in every
subsequent session into a remembered sensation. I think it is the single
highest-leverage change in the whole document after the measurement bet, and
it is a day of work.

---

## 4. The voice should be the user's — withdrawn

*This section was implemented and then removed. It is kept because the argument
against it is more useful than the argument for it was.*

The original claim: every guided track is a stranger pacing you through a
self-paced technique, so let people record the formulae themselves. It was
built — thirteen lines, stored on device, a third practice mode.

It was wrong, and the reason is one this document already contains. §1 says
every standard engagement mechanic is harmful here because the method's one
instruction is *do not try*, and §6 forbids a library because a catalogue makes
the ending commercially inconvenient. A set of your own recordings **is** a
personal library: it is an artefact that makes the app more yours and leaving
it more expensive. That is a retention mechanic, and it was built by the same
person who wrote the section forbidding them.

The deeper error was in the diagnosis. The problem was stated as "with your
eyes shut a line on screen reaches nobody" — true, and it does not argue for
audio. Someone practising eyes-closed in timer mode is *supposed* to be
issuing the phrase to themselves; that is the practice, not a gap in it. The
observation argues for the cues mattering less as you go, which the fade
already does. Enriching the scaffold was the opposite of the indicated move.

And a nicer voice is a stickier scaffold. Guided → timer → nothing works
because guided is mildly unsatisfying: a stranger's pacing is friction, and
friction is what makes people drop it on schedule. Removing that friction
without removing the crutch makes the crutch more comfortable to keep.

The genuine residue: an always-available audio path is an **accessibility**
requirement for anyone who cannot read the screen, and the synthetic guided
track already serves that. That is a different argument from training, and it
does not rescue self-recording.

## 4b. The voice should be the user's — the original argument

Every guided track is a stranger pacing you through a self-paced technique.
Two problems: the pacing is wrong for everyone except the average, and the
voice in your head during a self-suggestion exercise is somebody else's.

Have the user record the six phrases in their own voice during onboarding.

- It is autogenic in the literal sense.
- It removes the synthetic-voice problem permanently, in every language, with
  no TTS bill.
- Re-recording the phrase as the response develops is itself a good drill.
- It solves accent, gender and register in one move, for free.

Keep a synthetic voice as the fallback for anyone who does not want to hear
themselves, and for the explanatory films — which are teaching, not practice,
and where a narrator is correct.

Pair it with **haptics instead of speech for structure.** Eyes shut, a tap at
each phrase boundary carries the timing without words. The mature form of a
guided session is silence plus taps, which is also the exact shape the nidra
runner already takes.

---

## 5. Fix the ladder, and shorten it

The current ten steps are a clinical syllabus transplanted into an app. The
literature does not support the specific schedule: the eight-week,
one-exercise-per-week structure is a *course-scheduling artefact* from how the
method was taught in groups, and no trial establishes a dose-response
relationship for it. We inherited a timetable and treated it as a finding.

What I would change:

**Compress heaviness.** Right arm, left arm, both arms, legs is four steps and
four weeks for something the body largely does by transfer. Two steps —
dominant arm, then everything — is defensible and reaches warmth a month
sooner. Warmth is the first exercise that produces an unmistakable sensation
in most people, so time-to-warmth is arguably the metric the whole ladder
should be optimised against.

**Mass the first day, distribute after.** Three practices in the first hour,
not spread across it. The reason is not consolidation — the motor-learning
literature is mixed on that — it is that it establishes the behaviour while
motivation is at its peak, and produces three data points on day one instead
of one.

**Test transfer early.** The point of the method is a waiting room, not a
bedroom. Nothing currently tests that until step 10, which is far too late.
From week two, one of the three daily practices should be deliberately
non-ideal: sitting up, eyes open, somewhere noisy. Label it as such. A response
that only works lying down in a quiet room has not been trained, it has been
staged.

**Retrieve before re-exposing.** Before any guided audio plays, one tap: *what
is the phrase?* Retrieval practice is about the most robust finding in the
learning-science literature, it costs one screen, and we currently hand the
answer over for free every single time.

---

## 6. Anti-patterns: what to deliberately not build

Written as prohibitions because the pull towards each of them is strong.

**No streaks.** A streak converts a missed Tuesday into a loss, and loss
aversion is a form of trying. Show density, not continuity — a field of dots
where a gap is visibly unremarkable.

**Rate the effort, not the outcome.** The current log asks whether it landed.
Ask instead *how hard did you try* — and treat less as better. This inverts
the gradient: the user's own record starts rewarding the behaviour that
actually produces the response, rather than the outcome they cannot force.
Keep the landed/not-landed question, but demote it.

**No numbers during practice.** The countdown digits invite clock-watching.
The ring alone carries "this is progressing" without offering anything to
measure yourself against. Digits before and after; never during.

**No notifications that are just reminders.** Three-a-day pushes get muted in
four days, universally. The alternative is that the user names their own
anchors on day one — *after I sit down at my desk, before lunch, in bed* — and
the prompt quotes their words back. Better still, bind to context the phone
already knows: a gap between two calendar events is exactly the ninety seconds
this method was designed for, and nobody has to be nagged into it.

**No library.** The moment there is a catalogue of sessions to browse, this
becomes a content product and the ending becomes commercially inconvenient.

---

## 7. The middle: weeks two to ten

Everything above is about week one, and calling the rest "a syllabus" was a
dodge. The middle has its own failure modes, and they are not the same ones.

Week one's problem is *I feel nothing, is this working?* The middle's problems
are: the novelty is gone and the finish is not in sight, every new exercise
makes you a beginner again, the sequence grows while the clock does not, and
life happens.

### Three practices a day should not be three of the same practice

This is the change I would make first. Today all three daily practices are the
same growing stack, and by step eight the new element gets two of eight cue
slots — a quarter of the session — while five consolidated elements it does not
need to train take the rest. The instructional design is inverted: the thing
being learned gets the least exposure.

Split them:

| | What | Why |
|---|---|---|
| 1 | **The new element, alone, full time** | This is the training. It should get a whole session, not a corner of one. |
| 2 | **One earlier element, drawn at random** | Interleaving, and a guaranteed win on a bad day. |
| 3 | **The full sequence, briskly** | Integration. Once a day is enough for this. |

Same ninety seconds, three times, no extra cost. It also makes the three
distinguishable, and three identical repetitions a day are more boring than
three different ones — which is not a small point across nine weeks.

The interleaving has support: blocked practice (AAAA BBBB) produces faster
apparent gains and worse retention than interleaved, one of the better
replicated findings in motor learning. But it comes with a tension worth
naming rather than glossing: **interleaving reliably makes practice feel worse
while you are doing it**, and this product's main risk is people quitting
because they do not feel progress.

The resolution is which element you interleave. Do not mix *competing new*
material — draw the review from what is already consolidated. Then the second
practice is the one where something works, sitting in the middle of a week
where the new thing does not. Interleaving that reassures rather than
frustrates.

### Every step up feels like a step down — design that moment

You spend nine days getting heaviness reliable, and the reward is warmth,
which does not come. Repeated six times. Right now the app hands over a new
phrase and a briefing film and says nothing about this.

It should say it, using the user's own record: *"Heaviness took you nine days.
You are on day one of warmth. This is what day one felt like then, too."* A
generic reassurance is weak; their own history is not, and it gets stronger
every step. This is the one place where accumulated data earns its keep
emotionally rather than administratively.

### Gate on a probe, not on a rating

The current gate is days plus self-rated evidence. Both are reports about a
guided or timed session — so they measure the response *with the scaffolding
in place*, which is not the skill.

Add a **probe**: one session with no cues at all, a bell at each end, run it
yourself. That is the actual deliverable, tested. Passing the probe is what
should open the next step, and failing it is diagnostic rather than punitive —
it means the scaffold is doing work you think you are doing.

It also detects the classic failure of this method, which nothing currently
looks for: the formula degrading into recitation. Saying "my right arm is
heavy" without waiting for the arm is the most common way to practise
diligently for two months and learn nothing. A probe catches it; a rating
never will, because the person reciting believes they are practising.

### Shrink the phrase across the programme, not just in nidra

`PRIMED-NIDRA.md` specifies cue-shrinking — full wording, then compressed, then
one word — and it is built for the nidra runner. It belongs in the main ladder
too, and for the same reason: the endpoint of consolidation is a cue small
enough to cost nothing to issue. *My right arm is heavy* → *arm, heavy* →
*heavy* → a breath.

This is also what makes the endgame concrete in the middle. The scaffolding
visibly thins — guided, then timer, then silence, and the words themselves
getting shorter — so "you end up not needing this" stops being a promise on the
first screen and becomes something happening in front of you in week five.

### Lapses: design the return, and fix the floor

A nine-week programme will be interrupted. Illness, travel, a bad fortnight.
Three rules:

1. **Never show what was missed.** No "you missed 14 sessions". The record
   shows density; a gap is a gap and is allowed to be unremarkable.
2. **Return on a win, not where you left off.** Coming back after a week
   should offer one session of the last element that was solid, alone. Get the
   response back, then resume. Resuming cold on the hardest current material
   is how a lapse becomes a stop.
3. **Absence must not count as practice.** It currently does. `stepDays()`
   measures calendar days since the step began, so the floor is satisfied by
   elapsed time rather than by practice — two sessions, three weeks away, then
   three good days, and the gate opens on six days of actual work spread over
   twenty-four. Count days *practised*, and the same rule that protects the
   floor makes lapses harmless rather than silently rewarded.

### Put a landmark at the end of warmth

Nine weeks with one acknowledgement at the very end is too long a run. There is
a natural halfway house and it is not the numerical middle: it is the end of
warmth. Heaviness and warmth are the two exercises that do most of the work and
carry most of what evidence exists. Arriving there is worth marking — *you now
have the part that most people who learn this ever actually use* — with the
same handover tone as the closing film, not a celebration.

### Re-teach discharge where it actually happens

Autogenic discharge is explained once, after the first practice, and never
mentioned again. It becomes *more* likely deeper in — the warm centre and the
cool head are where unexpected emotion tends to turn up, in week six or seven,
a month and a half after the only time anyone mentioned it. The briefings are
already just-in-time by design; this should be too.

### Let the cautioned steps be skipped without failing

The heartbeat and the warm centre carry real cautions and are traditionally
taught in person. The path currently assumes all ten steps. Someone with a
heart condition or in pregnancy should be able to *finish* — "the first five"
is a legitimate and traditional endpoint — rather than stall against a step
they were correctly told to avoid. A programme that cannot be completed safely
by the people it warns is badly designed, not cautious.

### One weekly question

Daily ratings are for the gate. The useful reflection is weekly and
comparative: *compared with last week — easier, the same, or harder?* That is
the signal that detects a plateau, it costs one tap every seven days, and
nothing in the daily log surfaces it.

---

## 8. Design the ending, then put a door in it

The product's best and most unusual claim is that it finishes. Almost no
product-design vocabulary exists for this, which makes it a differentiator
nobody can copy without changing their business model.

- Show the ending from day one: a count of sessions remaining until the app is
  optional, visible and decreasing.
- The final deliverable is **not in the app**. It is a wallet card, a
  lock-screen image, a watch complication carrying six phrases. The app is
  scaffolding; ship the thing the scaffolding was holding up.
- At the end, offer to export the record and delete the app. Actually offer it.
  A product that means this is rarer, and more memorable, than any onboarding
  flourish.

And then the door: **the ending is where the nidra work belongs.** Someone who
has finished has an entry technique and nowhere to go with it — which is
precisely the gap `PRIMED-NIDRA.md` argues autogenic training has, and
precisely what nidra supplies. It should not appear anywhere before that point,
for the same reason a second instrument does not appear in week one of the
first. Right now it sits in Settings, which is where features go when nobody
has decided what they are.

---

## 9. Form factor

If the interaction is ninety seconds, eyes closed, three times a day, in
arbitrary places, then the phone is a compromise and the **watch is the correct
primary device**: it is already on the arm the exercise is about, it does
haptics natively, it measures pulse without being held, and it does not require
taking a slab of glass out in a waiting room.

I would not start there — the phone is where distribution and onboarding live —
but I would design the practice loop so that it can be lifted onto a wrist
without redesign, and I would treat the watch as the destination rather than a
companion.

---

## 10. What I would test first, in order

1. **Contrast induction on day one.** Cheap, no dependencies, and it either
   raises day-3 retention or it does not. Measure: proportion reaching practice
   four.
1b. **Split the three daily practices** into new / review / sequence. Also
   cheap, and it is the middle-game equivalent of the contrast drill: no new
   content, no extra minutes, a straight rearrangement of what already runs.
2. **Compressed heaviness** (two steps, not four). Measure: time-to-warmth and
   the drop-off between them.
3. **Self-recorded phrases.** Measure: completion, and whether people ever
   switch back to the synthetic voice.
4. **Pulse capture with post-hoc reveal.** The expensive one, with the legal
   question attached — which is why it is fourth, despite being the biggest
   potential win.

Every one of these is a change to the first week, because the first week is
where the product is decided.

---

## 11. What of this is built

Written after building most of it. Section by section:

| | Built |
|---|---|
| §3 contrast induction | yes — 43 seconds, offered before practice one, findable from Learn after |
| §4 the user's own voice | built, then **withdrawn** — see §4, it was a retention mechanic |
| §5 retrieval / transfer | transfer yes — the sequence practice is deliberately staged badly from step two. Retrieval-before-audio: no |
| §5 compressed heaviness | four steps to three — see below |
| §6 no numbers, no streaks, no library | yes |
| §6 anchored reminders | as calendar events, since a serverless PWA cannot schedule a notification |
| §7 all six middle-game changes | yes |
| §8 countdown, card, nidra as the door | yes |
| §2 measurement | **no — see below** |
| §9 watch | no, and not soon |

Two deliberate omissions, both flagged rather than quietly dropped.

**Compressing heaviness** happened, at three steps rather than the two argued
for here. The step that went is *both arms, in turn* — a whole week whose only
job was to show the response crosses to the other arm, which *both arms* shows
as well and at the same time. What remains is the dominant arm, where the
response is actually learned; both arms, where it generalises; and the legs,
where the classical formula lands and which mostly arrives free.

Two was not right. Merging the legs into the arms step changes the phrase
mid-step, and the phrase is the one thing this method holds invariant. Three
saves the week that was genuinely redundant and keeps the checkpoint that is
not, and the ladder is nine steps instead of ten.

**Measurement** is the biggest single win in this document and it is fourth on
the list for a reason: displaying physiology moves the product toward the
regulated end in several jurisdictions, and that needs a lawyer rather than an
afternoon. The technical part is real — camera PPG gives a defensible pulse
change across ninety seconds — but shipping it without the framing settled
would be the one genuinely reckless thing in here.

Everything else in this document is in the app.

## 12. What is still only theory

Nobody has used any of it. The instructional design is argued from the
literature and from first principles, the retention assumptions are guesses,
and the one number that would settle whether §2 matters — how many people reach
practice four — does not exist yet. `tools/test_journey.py` proves the app
works. It does not prove the programme does.
