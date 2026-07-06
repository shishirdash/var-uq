# var-uq — measurement uncertainty at the World Cup

Working repo for a blog series on the physics and uncertainty quantification
behind VAR's connected-ball touch sensor, anchored on the disallowed Croatia
goal against Portugal (2026 World Cup, round of 32) — a verdict that hinged on
a "heartbeat" blip from the IMU inside the ball.

Blog: [crudraven.notion.site](https://crudraven.notion.site/)

This repo is deliberately public *as part of the story*: the posts are
byproducts of an exploration done socratically with an AI assistant, and the
working artifacts — prediction logs, research notes with per-claim confidence
tags, simulation code, the iterated animation — are the evidence trail.

## Contents

- `OUTLINE.md` — series plan, milestones, plain-language glossary, status log
- `posts/` — post drafts (including the raw closed-book "brain-dump" skeleton
  the first post was built from)
- `sim/` — synthetic 500 Hz ball-IMU touch-detection Monte Carlo
  (`touch_detection.py`), generated figures, and the prediction-vs-result log
- `anim/decision-anim.html` — self-contained interactive schematic: the play
  and the offside rule, inside the ball, and the two detection channels
  ([view live](https://shishirdash.github.io/var-uq/anim/decision-anim.html))
- `research/` — sourced research notes (connected ball tech, cricket DRS,
  tennis electronic line calling), each claim tagged primary/journalism/unverified

## Running the simulation

```
cd sim
python3 -m venv .venv && .venv/bin/pip install numpy matplotlib
.venv/bin/python touch_detection.py   # regenerates figs/ and prints the sweep
```

Physics numbers are order-of-magnitude estimates; no official detection specs
(algorithm, thresholds, error rates) have been published by FIFA/Adidas/KINEXON
as of July 2026 — that gap is rather the point of the series.
