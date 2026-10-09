# identity-probe-toy

**What measuring an AI's identity continuity looks like — a method note
and a runnable toy. English | [简体中文](README.zh-CN.md)**

This is the method piece promised in the [organization
README](https://github.com/Idemstasis): how we think "identity
continuity" should be probed if it is to be **measured rather than
asserted** — plus a toy you can run in under a second (pure standard
library, no model, no network, deterministic) that demonstrates the
genre, and one of its characteristic traps: a consistency score alone
cannot tell *kept* from *re-given*; you also need provenance.

- **[docs/00_method.md](docs/00_method.md)** — the method note
  ([简体中文](docs/00_method.zh-CN.md))
- **[toy/00_identity_probe_toy.py](toy/00_identity_probe_toy.py)** — the
  runnable toy; full unedited output is reproduced in the method note

No third-party dependencies. Python 3.8+. Everything here is a
demonstration of a measurement genre, not evidence about any real
system — the note is explicit about what the toy refuses to show.

If you work on evaluation, dialogue systems, or agent memory, we would
genuinely like to be told where this frame is naive: open a thread in
**GitHub Discussions under this organization**.

*The name states the question. It does not answer it.*
