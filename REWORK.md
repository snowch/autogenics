# The rework

The agreed architecture for the rebuilt session model, and why each part is the
way it is. Written down because it had been living in a conversation.

Status: scripts written (`script/seg-*.md`), model and container built behind
`?v=2`. Nothing here has replaced the shipping app.

---

## The session is a container of layers

```
posture → the round → the formula stack → the close
```

Fixed, in that order, every session. The bookends are **structure**: they always
run, whatever the app has stopped saying. Only the narration inside them fades.

**Every part is a layer**, and a layer is a thing that gets taught once, fades as
you repeat it, and stays available to go back to. Position is layer 0 — the
first thing anybody learns and the first to go quiet, because it is in every
session and "sit back, or lie down" does not need saying for the twenty-first
time.

That is the whole model. Nothing in the app is a setting; it is a layer at some
stage of being learned.

## Position is taught, not chosen

A picker was the wrong shape. It treats position as a preference when it is the
first lesson, and the three positions are a sequence rather than options:

| | when | why it exists |
| --- | --- | --- |
| Lying down | learning, and the sleep variant | easiest for heaviness, easiest to fall asleep in |
| Back in a chair | the workhorse | supported and sustainable |
| Sitting forward | a train, a waiting room | no back support needed — this is what makes "anywhere" true |

They arrive in that order, which is the transfer arc the app already commits to:
the sequence practice is deliberately staged badly, sitting up, wherever you
happen to be, so a response that only works lying down somewhere quiet is caught
early rather than at the last step. Free choice comes at the end, when you know
all three and the circumstances decide.

## Fade is per layer, and so is restore

```
reps(layer)  = sessions containing that layer, ladder only, excluding rescue
fade(layer)  = S.fade[layer] ?? tier derived from reps(layer)
```

Fade is a **pure function of the log**, recomputed on every read, never stored —
a stored count drifts the moment anything filters differently, and "restore the
guidance" would have to unwind it. Rescue is excluded by construction rather
than by a flag somebody remembers to set: a rescue session simply never carries
`program:'ladder'`.

Restoring guidance is a write to `S.fade[layer]` and is non-destructive. Reps
keep accruing underneath, so clearing it returns you to where they say you are.
That is "go back to a previous lesson" — for one layer, not for everything.

### A layer shrinks, it does not switch off

Position is what made this obvious. Once you know it, it does not disappear —
it becomes one line. *Get into position, then we scan.* So a layer is not
taught-or-gone; it has three rungs, and the segment keeps its full duration at
every one, because getting into position takes as long as it takes whether or
not you are being told how. **The container never fades; only the words do.**

| layer | under 8 reps | 8–19 | 20+ |
| --- | --- | --- | --- |
| Position | the full narration | Into position. Hands where they fall. | Position. |
| The round | teaching pass, then the places | the twenty-five places | nothing — you run your own |
| A formula | lead-in, then the phrase | the phrase | the short form, then one word |
| The close | briefing, then three cues | three cues | Take it back. |

This is not a new mechanism. It is the app's existing convention, already
implemented three times at the same thresholds:

```js
const shrink = (full,mid,mature) => n => n<8 ? full : n<20 ? mid : mature;
const shrinkCue = c => { … n<8 ? c : n<20 ? f[0] : f[1] };
DRILLS[].c = ['the long form…', 'shorter…', 'Two words.']
```

The container layers were the only things built as a binary, and that was the
error. Eight and twenty are the app's numbers and there is no reason for new
ones.

**The close never reaches the last rung.** Every other layer ends at silence and
you run it yourself; the close keeps a line for ever, because it is the only
part of the practice with a caution attached and the onboarding promises the app
always runs it. One line is a cheap price for not quietly dropping the thing
that stops you standing up light-headed.

### The tiers, and the inversion at the end

| tier | what the app does |
| --- | --- |
| guided | voice, cues, a chime at every section |
| timer | cues on screen, a chime at each section |
| silent | one chime to begin. Nothing on screen, no marks, no end. |

Section chimes survive the voice going — that is how you know to leave the round
and start the formula. They cannot survive the silent tier: a round run slightly
slow gets a chime through the middle of it, which is worse than no mark at all.

So at the last tier **the app stops setting the length and starts measuring it**.
You tap when you have finished and it records what you took. That is the first
honest number it holds — your own pace, unprompted, rather than a duration it
handed you. It is also where the probe went: a session with nothing playing and
nothing to look at was a one-off ceremony gating the ladder, and here it is
every session.

## Two kinds of session

Only one formula in a stack is training; the rest are recall. But the fix is not
to run them faster — see `script/seg-formulae.md` — it is two kinds of session,
which is `DESIGN.md` §7's own answer and shipped here once already as
new / review / sequence.

| | stack | at stage 6 | how often |
| --- | --- | --- | --- |
| Training | the stage's own formula, alone | 3:22 | 2–3× daily |
| Sequence | every formula, in order | 9:22 | once daily |
| Rescue | none — the container alone | 2:10 | whenever |

Every formula runs at six repetitions, ten seconds apart. There is no principled
reason a formula you already hold gets a worse gap than the one you are
learning; the gap is the exercise in both cases.

## Programmes

- **Foundation** — the container plus heaviness in the dominant arm. Short, four
  to six times a day. Completes and opens the ladder.
- **The ladder** — the six standard exercises, one added per stage.
- **Rescue** — the container with an empty stack. Permanently guided, never
  fades, never graduates, one tap away, logged apart from everything else.

Gating is soft and self-attested. Nothing counts: the criterion is stated, your
own record sits under it, and the button is always there.

## Naming

The architecture keeps its vocabulary in the ids and in this file. The screen
says what you are about to do. So *rescue* is "The round on its own", *foundation*
is "One arm, heavy", and no user-facing string says Foundation, Rescue, sakshi,
pranamaya, Schultz or Kermani.

Two rules underneath that:

- **Sensation teaches; description does not.** "Heaviness" is precise after the
  clench-and-release drill and actively misleading before it — out of context,
  *my arms feel heavy* is a complaint you would take to a doctor. So: never put
  a name in front of somebody before the thing it names has been felt.
- **Say what a thing is before saying how it is gated.** Both track captions used
  to explain the rule and never the track.

## What is settled, and what is not

Settled: the container, the round (Kermani's order, our words, bilateral,
twenty-five places at four seconds), the two rates question, two kinds of
session, the tier ladder, per-layer fade, position as layer 0.

Open:

- Whether three positions or two, with lying down reserved for the sleep
  variant. Lying down trains heaviness fastest and is also the one that turns
  the practice into a nap.
- Whether narration gets recorded at all, or the container stays silent with the
  words on screen. Deferred until the silent version has been lived with.
- Foundation's completion criterion, stated but not yet worded.
