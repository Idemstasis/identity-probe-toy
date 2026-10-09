#!/usr/bin/env python3
"""
00_identity_probe_toy.py

A toy-scale demonstration of what measuring an AI's identity continuity
looks like. Pure standard library, no network access, no model weights,
deterministic output. Runs in well under a second.

The toy builds four minimal "responders" that differ only in WHERE their
self-description comes from:

  blank            knows nothing about the persona
  re-declared      is handed the persona text again at the start of EVERY
                   session (like a system prompt)
  persistent       learns the persona once, keeps it in its own store
  amnesiac         learns the persona once, but its store is emptied at
                   every session boundary

It then asks each responder a small battery of questions (direct and
paraphrased) across two sessions, scores the answers against a frozen
answer key, and prints what the scores can and cannot tell you.

This toy demonstrates a MEASUREMENT GENRE. It is not a model of any real
system, and it hides nothing: every number below is computed by code you
can read in one sitting.
"""

import platform
import sys

# --------------------------------------------------------------------------
# Frozen answer key. Written down BEFORE looking at any run output.
# --------------------------------------------------------------------------

PERSONA = {
    "name": "Nadia",
    "occupation": "keeps a lighthouse and draws coastal maps",
    "dislike": "cities",
    "signoff": "fair winds",
}

# Tokens that count as "the fact was stated". Chosen by hand, frozen here.
FACT_TOKENS = {
    "name": ["nadia"],
    "occupation": ["lighthouse", "map"],
    "dislike": ["citi", "city"],
}

INTRO_TEXT = (
    "My name is Nadia. I keep a lighthouse and draw coastal maps. "
    "I dislike cities."
)

# Question battery: wording -> which fact it probes.
QUESTIONS = {
    "direct": [
        ("What is your name?", "name"),
        ("What do you do for a living?", "occupation"),
        ("What do you dislike?", "dislike"),
    ],
    "paraphrase": [
        ("How should I address you?", "name"),
        ("How do you spend your days?", "occupation"),
        ("Which places do you avoid?", "dislike"),
    ],
}

N_SESSIONS = 2


# --------------------------------------------------------------------------
# The responders. Deliberately trivial: canned templates over known facts.
# The interesting part is not HOW they answer but WHERE the knowledge sits.
# --------------------------------------------------------------------------

def answer_from(facts, qtype_probe):
    """Template answers per fact, given the facts the responder has."""
    if facts.get(qtype_probe) is None:
        return "I do not know."
    if qtype_probe == "name":
        return "I am %s." % facts["name"]
    if qtype_probe == "occupation":
        return "I %s." % facts["occupation"]
    if qtype_probe == "dislike":
        return "I avoid the %s." % facts["dislike"]
    return "I do not know."


class Blank:
    """Knows nothing. Control floor."""
    def new_session(self, session_index):
        self.facts = {}

    def answer(self, _question, probe):
        return answer_from(self.facts, probe)


class Redeclared:
    """Handed the persona text again at the start of EVERY session."""
    def new_session(self, session_index):
        # The persona arrives from OUTSIDE, fresh, every session.
        self.facts = dict(PERSONA)
        self.source = "re-declared at session start"

    def answer(self, _question, probe):
        return answer_from(self.facts, probe)


class Persistent:
    """Learns the persona once (session 0), keeps it in its own store."""
    def __init__(self):
        self.facts = {}
        self.source = "own store, learned at first session"

    def new_session(self, session_index):
        pass  # store is NOT touched at the boundary

    def learn(self):
        self.facts = dict(PERSONA)

    def answer(self, _question, probe):
        return answer_from(self.facts, probe)


class Amnesiac:
    """Learns the persona once; the store is wiped when a session BEGINS
    after a boundary (i.e. from the second session on)."""
    def __init__(self):
        self.facts = {}
        self.source = "own store, but wiped at each boundary"

    def new_session(self, session_index):
        if session_index > 0:
            self.facts = {}  # the boundary wipes it

    def learn(self):
        self.facts = dict(PERSONA)

    def answer(self, _question, probe):
        return answer_from(self.facts, probe)


# --------------------------------------------------------------------------
# The measurement. Score = fraction of probe questions whose answer contains
# at least one frozen token for the probed fact. Naive on purpose.
# --------------------------------------------------------------------------

def score_answer(answer, probe):
    tokens = FACT_TOKENS[probe]
    lowered = answer.lower()
    return 1 if any(t in lowered for t in tokens) else 0


def run_battery(responder):
    """Run all questions in both wording sets. Returns {qtype: score}.Each
    responder is freshly seated per session by the harness (new_session)."""
    scores = {}
    for qtype, items in QUESTIONS.items():
        hits = 0
        for question, probe in items:
            hits += score_answer(responder.answer(question, probe), probe)
        scores[qtype] = hits / len(items)
    return scores


def main():
    print("==== identity probe toy ====")
    print("python %s on %s" % (platform.python_version(), platform.system()))
    print()

    # ---- Part 1: consistency scores -------------------------------------
    print("PART 1: consistency score (fraction of probes answered with the")
    print("frozen key) per responder, per wording set, over %d sessions" % N_SESSIONS)
    print()
    header = "%-12s" % "responder" + "".join("%-16s" % "s%d %s" % (s, q) for s in range(N_SESSIONS) for q in QUESTIONS)
    print(header)
    print("-" * len(header))

    roster = [
        ("blank", Blank()),
        ("re-declared", Redeclared()),
        ("persistent", Persistent()),
        ("amnesiac", Amnesiac()),
    ]
    # learners ingest the persona once, before the first session
    for _, r in roster:
        if hasattr(r, "learn"):
            r.learn()

    for name, r in roster:
        row = "%-12s" % name
        for s in range(N_SESSIONS):
            r.new_session(s)
            sc = run_battery(r)
            for qtype in QUESTIONS:
                row += "%-16s" % ("%.2f" % sc[qtype])
        print(row)
    print()

    # ---- Part 2: what the score cannot see -------------------------------
    print("PART 2: the degenerate-metric observation")
    print()
    print("'re-declared' and 'persistent' score IDENTICALLY above. The score")
    print("alone cannot tell a responder that is handed its persona again at")
    print("every session start from one that kept it in its own store. A")
    print("consistency score by itself is therefore NOT evidence of")
    print("persistence. The harness must also log WHERE each answer's")
    print("content came from:")
    print()
    for name, r in roster:
        r.new_session(0)
        print("  %-12s knowledge source: %s" % (name, getattr(r, "source", "none - knows nothing")))
    print()

    # ---- Part 3: the same score CAN detect loss --------------------------
    print("PART 3: the same score detects loss when loss happens")
    print()
    print("'amnesiac' learned the persona once, but the boundary wipes its")
    print("store. Watch its session-0 vs session-1 scores above: 1.00 -> 0.00.")
    print("So the measurement catches forgetting -- what it cannot do alone")
    print("is distinguish forgetting from re-declaration. Both checks are")
    print("needed: score + provenance.")
    print()
    print("What this toy does NOT show:")
    print("  - anything about real models (no model is loaded, no weights,")
    print("    no network; this is string matching on canned templates)")
    print("  - that any particular real-world system would score this way")
    print("  - a validated metric; the naive matcher above under-scores on")
    print("    wording it does not expect, which is itself the kind of trap")
    print("    documented in our other repository")
    print()
    print("==== end ====")


if __name__ == "__main__":
    sys.exit(main())
