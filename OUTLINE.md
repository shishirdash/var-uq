# VAR under uncertainty — blog series outline

Working theme: a tournament-deciding, binary verdict produced from a continuous noisy
measurement, with no error bars shown to anyone. ML + UQ + physics for a lay reader.

Anchor event: Croatia–Portugal, 2026 World Cup round of 32 (Jul 2, Toronto). Gvardiol's
103rd-minute equalizer disallowed because the Trionda ball's IMU registered a graze off
Matanović (possibly his hair), making Pašalić offside. Referee ruled on the sensor alone;
FIFA published no thresholds or error rates.

Style: `blog` profile (first-person, warm, self-deprecating, em-dashes OK, anecdote
framing, optimistic close) + `personal` profile's curious-reader stance. Readable to a
lay outsider; define every technical term on first use.

## Post 1 — "The hair that ended a World Cup run"

Narrative anatomy of the decision. The play, the heartbeat graphic, then a lay-friendly
tour of the tech stack (ball IMU at 500Hz, semi-automated offside limb tracking, sensor
fusion) and every place uncertainty enters the pipeline. Curious, not prosecutorial.
Sets up the question posts 2–3 answer.

## Post 2 — "Can a chip in a ball feel a hair?"

The R&D post. Fermi estimates (a hair graze is ~1000× smaller impulse than a header),
then a synthetic-IMU simulation: inject graze pulses into realistic aero noise, run a
detector, produce ROC curves and a detectability map over (impulse, contact time).
Key honest modeling point: rigid-body deceleration vs. shell-vibration "ring" — the
latter is probably what makes detection feasible, and its coupling is the big unknown.
Conclusion is whatever the physics says. Sim lives in `sim/`.

## Post 3 — "How sports measure doubt"

Comparative and descriptive, NOT prescriptive (no soccer policy takes).
- Cricket DRS: umpire's call = uncertainty made explicit in protocol; snicko/UltraEdge
  as the direct analog of the heartbeat graphic.
- Tennis: Hawk-Eye / electronic line calling — ~mm-scale mean error presented as
  certainty by fiat (Collins & Evans "false transparency" prior art).
- Soccer's own internal spectrum: goal-line tech (pure measurement) → offside line
  (measurement + ML pose models) → touch detection (signal detection) → handball /
  dangerous play (pure human judgment; "clear and obvious" as a crude uncertainty
  protocol).
Ends with open questions, not policy.

## Woven thread (all posts) — "how I built this with an AI"

Short "workshop notes" sidebars per post, drawn from actual usage during this project:
parallel research subagents fanned out while the main thread built the sim, model/effort
switches for derivation vs. prose work, etc. If enough material accumulates, promote to
a capstone post 4.

## Milestones (adaptive — Shishir's answers reshape these)

- M0 — Understand the decision. ✅ DONE 2026-07-06. Socratic walk through the Matanović
  call: rule → two physical channels (push vs ring) → noise environment → frequency
  separation → threshold detection. All reconstructed by Shishir via Fermi estimates.
  Remaining deliverable: one-page "anatomy of the decision" (Shishir brain-dumps the
  chain in his own words, Claude edits) → skeleton of post 1. Not blocking.
- M1 — Physics of the measurement. ← WE ARE HERE. Predict-then-check against the sim:
  Shishir predicts each result before it's revealed; divergences drive model revisions.
  First prediction pending (question 6). Deliverable: revised sim + figures + a
  prediction-vs-result log → post 2 and the meta-thread.
- M2 — Cross-sport comparison. Work through the cricket/tennis research (banked in
  research/); build the measurement→judgment taxonomy. Deliverable: comparison table +
  post 3 skeleton.
- M3 — Drafting. Posts 1→2→3 in blog style, workshop-notes sidebars from actual logs.

Pace rule: one socratic question at a time; milestone gates move on Shishir's answers,
not on artifact completion.

## Plain-language glossary (terms we keep using)

- IMU: inertial measurement unit — the chip in the ball. Feels its own motion only
  (accelerometer = jolts, gyroscope = spin). No microphone, no camera. 500 samples/s.
- The push (channel 1): the graze's momentum change. Shishir's Fermi result: deflects
  the ball ~0.05–1 mm over the remaining flight — invisible to eye, camera, and
  (nearly) the chip.
- The ring (channel 2): the shell vibrating after contact, like a drum — sound traveling
  through the ball's skin. Fast (~hundreds of Hz), outlives the 5 ms contact.
- kappa (κ): sim knob for how much of the ring reaches the chip. 0 = none (chip
  feels only the push); 2 = arrives loud. Still unpublished, but the 2026 Trionda
  embeds the chip IN one panel's layer (Adidas primary, verified 2026-07-06; earlier
  balls suspended it at the center) — direct shell mounting shifts the κ prior up,
  and adds a "which side did the graze land on" variance term.
- Noise floor: the flicker the chip feels all flight anyway (spin wobble ~10 Hz +
  turbulent buffeting), all below ~80 Hz, roughly 1 m/s² in size.
- The detector: high-pass at 100 Hz (ignore the noise band), then threshold tuned to
  1% false alarms. Shishir re-derived this design in the M0 dialogue.
- Predict-then-check ("sealed envelope"): sim results stay hidden until Shishir has
  predicted them; then we compare. Divergence = learning material.
- Fermi estimate: order-of-magnitude reasoning with chosen-not-known numbers, carried
  as brackets (ranges), not points.

## Status log

- 2026-07-05: incident researched + grounded (ESPN/Goal/TNT). Outline agreed.
  Sim build started; 3 research agents launched (cricket DRS, tennis ELC, connected
  ball tech specs).
- 2026-07-05 (later): sim v1 runs, self-checks pass; figures in sim/figs/. Socratic
  loop opened with Shishir (4 questions pending his predictions before revealing
  run-1 results). Ball-tech + tennis findings banked in research/ (headline: NO
  published algorithm, threshold, or error rate anywhere — confidence claims only;
  Collins & Evans 2008 citation verified, they proposed showing confidence
  intervals). Cricket findings banked (headline: umpire's call + the 300cm/40cm
  auto-deference rules literally encode error propagation in the playing conditions;
  Hawk-Eye's founder on record calling it a legacy uncertainty compromise). Research
  phase COMPLETE — all three agents reported.
- Working mode (per Shishir): socratic co-exploration, predict-then-check. No
  one-shot deliverables.
- 2026-07-06: M0 completed via socratic dialogue (see glossary). Trionda sensor
  placement VERIFIED primary (side-mounted in one panel + counterweights; Adidas
  release) — κ prior up, geometry-lottery variance term added. SciAm Trionda
  geometry piece banked. Envelope 1 opened: Shishir predicted 1/100 (push) and
  99/100 (loud ring) vs sim 8/100 and 100/100 — logged in sim/prediction-log.md;
  key unpredicted finding: detection is a CLIFF (κ=0.5 ≈ push-only).
- Animation decision-anim.html iterated v1→v6 with Shishir's design feedback
  (final: rotated tactical-board view, true-scale box, verdict as HTML callout,
  compressed corridor for Perišić). All frames render-verified via browser.
- 2026-07-06 (later): animation verified against Shishir's broadcast screenshots
  (Fox, 103:09–103:18, 6 frames). Fixed: kit colors (Croatia white, Portugal navy,
  GK yellow, officials orange), graze zone (central, box edge), Gvardiol finish
  (close-range slide ~10 m, late run kept onside at the layoff), defensive-line
  collapse after the graze + a frozen "line at the graze" ghost in the verdict
  (the SAOT freeze-frame concept, visualized). Real sequence duration ≈ 9 s,
  matching the animation's play phases.
- 2026-07-06 (day 2): Round-2 opened (predicted 0.2 vs ~0.35 mN·s cliff; logged).
  κ=2 panels added to all figures. Traces flaw found by Shishir and fixed (HPF
  overlay). Post-1 skeleton brain-dump completed (closed book) → draft assembled
  with drift corrections. Repo pushed PUBLIC to github.com/shishirdash/var-uq;
  GitHub Pages live — animation at
  https://shishirdash.github.io/var-uq/anim/decision-anim.html (embed URL now in
  the post draft). Notion MCP added user-scope; publish deferred to next session
  (/mcp auth needed). Blog reboot direction agreed: "Explorations" section,
  transparent AI-collaboration framing.
- PENDING: Shishir's TODOs — broadcast waveform frame-grab, voice pass on draft.
  Then: Notion publish (next session), M1 round 3 (contact-duration cliff),
  M0 anatomy one-pager, M2 comparison, post 2.
