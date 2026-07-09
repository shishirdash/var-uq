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

## Roadmap v3 (agreed 2026-07-08, supersedes v2): soccer-first series

Stick with the soccer/VAR thread end to end; sprinkle analogies or contrasts
with other sports where they teach, but park the full cross-sport treatment
until after post 5. Order: sims → posteriors → JEPA → real-video validation →
other sports.

## Post 1 — "On offsides and uncertainty" (PUBLISHED 2026-07-08)

Anatomy of the decision, now covering ALL THREE channels: the push and the shudder
(accelerometer) plus the twist (gyroscope — discovered via Shishir's own question,
round 3). The rule, the chip, the three physical traces, κ and f as the twin
unmeasured couplings. No sim details (post 2's job).

## Post 2 — "Tinker, Tailor, Sampler, Spy" (the simulation ritual)

The step-by-step detection ritual, visualized per channel: innocent trials set the
threshold, guilty trials climb it, the sigmoid draws itself, the cliff emerges.
Psychometric-curve fitting + adaptive sampling for precise cliffs with CIs. The
playable-cliff interactive. Payoff sections brought forward from round 4
(2026-07-08): the disagreement curve 2p(1−p) (verdict instability between
matches; zone width per channel) and the beep/silence likelihood-ratio
asymmetry (50× vs ~2× — convicting on a beep is defensible, exonerating on
silence is not; Gvardiol call sat on the strong side). LR-only here; the
prior-odds/posterior step stays post 4. Scaling laws via dimensional analysis (flight speed etc.
collapse into ~3 dimensionless ratios). Finale: the JOINT sim — one graze, both
sensor streams, fusion detector hedging the κ-vs-f lottery. Prediction-log excerpts
as the honest thread. Kitchen experiment (phone IMU in/on a real ball) feeds the
model's ring-frequency and κ inputs if done in time.

## Post 3 — "Verdicts as posteriors" (hierarchical Bayes)

κ, f, J unknown per touch with priors; the trace yields a POSTERIOR probability of
touch, not a binary. Build the object Collins & Evans (2008) said broadcasters
should show. Hierarchical structure: population priors over touches, per-incident
inference. The Matanović call re-run as a posterior.

## Post 4 — "Can a world model learn the ball?" (JEPA exploration)

Train a small self-supervised embedding-predictor (JEPA-style) on synthetic
touchless flights; test whether prediction-error spikes at grazes and whether the
latent encodes spin/decay/κ unprompted. We hold the answer key (we wrote the
physics), so we can grade what the world model "discovered" against the socratically
derived detector. Doubles as Shishir's JEPA learning goal.

## Post 5 — "Validation from real video" (new in v3)

Confront the sims with reality: digitize the broadcast heartbeat waveform
(frame-grab → trace) and compare its shape/timing against the synthetic shudder;
kitchen IMU experiment (phone in/on a real ball) to ground the sim's inputs —
shudder frequency, noise floor, κ ranges. Honest scoring: which sim assumptions
survived contact with data, which didn't. (Validation artifacts can start
accumulating earlier — they feed sim inputs for posts 2–4.)

## Post 6 — "How sports measure doubt" (parked until after post 5)

Comparative and descriptive, NOT prescriptive (no soccer policy takes).
- Cricket DRS: umpire's call = uncertainty made explicit in protocol; snicko/UltraEdge
  as the direct analog of the heartbeat graphic.
- Tennis: Hawk-Eye / electronic line calling — ~mm-scale mean error presented as
  certainty by fiat (Collins & Evans "false transparency" prior art).
- Soccer's own internal spectrum: goal-line tech (pure measurement) → offside line
  (measurement + ML pose models) → touch detection (signal detection) → handball /
  dangerous play (pure human judgment; "clear and obvious" as a crude uncertainty
  protocol).
Ends with open questions, not policy. Until then, other sports appear only as
sprinkled analogies/contrasts inside the soccer posts. Research stays banked in
research/.

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
- M1.5 — The twist (gyro channel). ✅ DONE 2026-07-07 socratically: decomposition →
  Δω ceiling → two-window detector → Allan-U limits → detrend fix → cliff at ~0.23
  (f=1) / ~0.7 (f=0.3). Logged as round 3.
- M2 — Post 2 sim ritual: sigmoid/cliff fitting, disagreement-zone widths,
  beep/silence asymmetry section, joint/fusion sim, playable-cliff interactive.
- M3 — Advanced arcs, per roadmap v3 order: post 3 (hierarchical Bayes) then
  post 4 (JEPA world model), each preceded by its own socratic exploration phase.
- M4 — Real-video validation (post 5): waveform digitization + kitchen IMU;
  artifacts can start accumulating during M2–M3.
- M5 — Cross-sport comparison (post 6, parked): work through the cricket/tennis
  research (banked in research/); build the measurement→judgment taxonomy.
- Supporting builds queued: joint 3-channel sim + fusion detector; psychometric
  cliff-fitting; scaling-law derivation; kitchen IMU experiment; broadcast-waveform
  digitization (validation).

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
- 2026-07-06 (later): PUBLISHED to Notion. /mcp re-auth to correct workspace
  ("TL;DR"); post 1 created under Explorations (Shishir had already created the
  section and moved the old data-roles post into it). Page includes house-style
  TL;DR callout, waveform-placeholder callout, workshop-notes callout, and the
  animation embedded as a sandboxed HTML attachment (+ GitHub Pages link).
  Notion page: app.notion.com/p/395b6a00c28a81ae9fd0e9ebc9f9a080
- 2026-07-06 (evening): BLOG REBRANDED by Shishir: "TL;DR" → "Socratic Parroting"
  (his synthesis of the stochastic-parrots riff + socratic format). What/Why/Who
  replaced with a minimal toggle: "Explorations on (and with) AI, tech, books,
  etc." + 4-line bio. No gimmicks policy for new posts: TL;DR callout removed from
  post 1; workshop-notes callout flattened to a plain section. Post 1 remains
  PRIVATE pending his TODOs. Framing critique saved at
  ../tldr-framing-critique.md (outside public repo, deliberately).
- 2026-07-08: 🚀 POST 1 PUBLISHED — "On offsides and uncertainty" live under
  Explorations on crudraven.notion.site (Socratic Parroting). Final form: three
  channels + κ_push/κ_shudder/κ_twist taxonomy, two detection-rule sections,
  translation-dictionary table, 5 footnotes (process, Trionda, Nyquist, the ride,
  MEMS tremble mechanisms), orange links, embeds from both animation variants.
  Route to publish: 3 socratic milestones, 3 critic-panel rounds (6 personas),
  fact-check green, author voice passes throughout.
- NEXT: post 2 ("Tinker, Tailor, Sampler, Spy") — the sim ritual. Queued builds:
  joint 3-channel sim + fusion detector, psychometric cliff-fitting, scaling laws,
  playable-cliff interactive, kitchen IMU experiment, waveform digitization.
  Then: Notion publish (next session), M1 round 3 (contact-duration cliff),
  M0 anatomy one-pager, M2 comparison, post 2.
