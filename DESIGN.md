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

## 4. The voice should be the user's

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

## 7. Design the ending, then put a door in it

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

## 8. Form factor

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

## 9. What I would test first, in order

1. **Contrast induction on day one.** Cheap, no dependencies, and it either
   raises day-3 retention or it does not. Measure: proportion reaching practice
   four.
2. **Compressed heaviness** (two steps, not four). Measure: time-to-warmth and
   the drop-off between them.
3. **Self-recorded phrases.** Measure: completion, and whether people ever
   switch back to the synthetic voice.
4. **Pulse capture with post-hoc reveal.** The expensive one, with the legal
   question attached — which is why it is fourth, despite being the biggest
   potential win.

Every one of these is a change to the first week, because the first week is the
product. The remaining nine are a syllabus, and syllabuses are the easy part.
