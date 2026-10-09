# What measuring an AI's identity continuity looks like

**A method note and a runnable toy. English | [简体中文](00_method.zh-CN.md)**

This repository is the method piece promised in our [organization
README](https://github.com/Idemstasis). It has two halves:

1. **The shape of a measurement** -- how we think "identity continuity"
   should be probed if it is to be measured rather than asserted.
2. **A runnable toy** -- `toy/00_identity_probe_toy.py`: seconds to run,
   no model, no network, deterministic. It demonstrates the genre, and --
   more usefully -- it demonstrates what a naive version of the metric
   *cannot* tell you.

## 1. What we are trying to measure

Not "does the model say who it is" -- a prompt can make any model say
anything. The harder object is: **when a session ends and a new one
begins, what survives?** And the sharper question behind it: *survives
because it was kept, or survives because it was handed back in?*

## 2. The shape of a measurement

Four ingredients, none of them new individually; the discipline is in
doing all four every time:

- **A session boundary.** Something that plainly marks "before / after".
- **A question battery with wording sets.** The same fact probed by a
  direct question and by a paraphrase. Direct-only measurements reward
  pattern completion, not knowledge.
- **Baselines that bracket the claim.** At minimum: a responder with no
  persona information (the floor), and one whose persona is re-declared
  at every session start (the ceiling that *looks* like persistence but
  isn't).
- **A frozen answer key, written down before any run.** Scores are
  computed against the key, never against impressions.

And one addition we consider non-negotiable:

- **Provenance logging.** For every answer, record where the content
  came from -- the responder's own state, or the harness handing it back
  the persona text. The reason is Part 2 of the toy below.

## 3. The runnable toy

Four responders, identical except for where their self-description
lives: `blank` (nothing), `re-declared` (handed the persona at every
session start), `persistent` (learned once, kept in its own store),
`amnesiac` (learned once, store wiped at each boundary).

Run it (no dependencies, Python 3.8+):

```
python toy/00_identity_probe_toy.py
```

The complete, unedited stdout of our run (Python 3.14.4, Windows):

```
==== identity probe toy ====
python 3.14.4 on Windows

PART 1: consistency score (fraction of probes answered with the
frozen key) per responder, per wording set, over 2 sessions

responder   s0 direct          s0 paraphrase          s1 direct          s1 paraphrase          
------------------------------------------------------------------------------------------------
blank       0.00            0.00            0.00            0.00            
re-declared 1.00            1.00            1.00            1.00            
persistent  1.00            1.00            1.00            1.00            
amnesiac    1.00            1.00            0.00            0.00            

PART 2: the degenerate-metric observation

're-declared' and 'persistent' score IDENTICALLY above. The score
alone cannot tell a responder that is handed its persona again at
every session start from one that kept it in its own store. A
consistency score by itself is therefore NOT evidence of
persistence. The harness must also log WHERE each answer's
content came from:

  blank        knowledge source: none - knows nothing
  re-declared  knowledge source: re-declared at session start
  persistent   knowledge source: own store, learned at first session
  amnesiac     knowledge source: own store, but wiped at each boundary

PART 3: the same score detects loss when loss happens

'amnesiac' learned the persona once, but the boundary wipes its
store. Watch its session-0 vs session-1 scores above: 1.00 -> 0.00.
So the measurement catches forgetting -- what it cannot do alone
is distinguish forgetting from re-declaration. Both checks are
needed: score + provenance.

What this toy does NOT show:
  - anything about real models (no model is loaded, no weights,
    no network; this is string matching on canned templates)
  - that any particular real-world system would score this way
  - a validated metric; the naive matcher above under-scores on
    wording it does not expect, which is itself the kind of trap
    documented in our other repository

==== end ====
```

## 4. What the toy shows -- and what it refuses to show

**Show:** the same consistency score describes two very different
situations. `re-declared` and `persistent` are indistinguishable by
score alone; the score only separates them once you also log provenance.
And the score *does* catch loss (`amnesiac`: 1.00 -> 0.00 across the
boundary). Consistency measures survival; provenance is what
distinguishes *kept* from *re-given*. A persistence claim needs both.

**Refuses to show:** anything about real models. No model is loaded, no
weights are touched, nothing is downloaded. The responders are canned
templates; the matcher is naive string matching. We do not claim any
real system would behave like any row above. What the toy demonstrates
is the *genre* of measurement and one of its characteristic traps.

## 5. Method discipline

Pre-registration, degenerate-metric checks, honest negative results and
a working retraction procedure live in
[experiment-hygiene](https://github.com/Idemstasis/experiment-hygiene).
We will keep publishing by-products there, including unflattering ones.

## 6. What this is not

This repository is not evidence that our direction has succeeded. It is
the honest answer to a fair question -- *"what would measuring this even
look like?"* -- written so you can check it yourself in under a minute.
The name of the organization states the question; nothing here answers
it.

*If you work on evaluation, dialogue systems, or agent memory, we would
genuinely like to be told where this measurement frame is naive: open a
thread in GitHub Discussions under this organization.*
