# Prediction-vs-result log (M1 deliverable — raw material for post 2 + meta-thread)

## Round 1 — 2026-07-06: "out of 100 optimistic grazes (J=1 mN·s), how many detected?"

| Case | Shishir predicted | Sim result | Verdict |
|---|---|---|---|
| push only (κ=0) | 1/100 | 8/100 | right instinct ("blind floor"); pulse edge-leakage above 100 Hz explains the extra 7 |
| loud ring (κ=2) | 99/100 | 100/100 | essentially exact |

Unpredicted findings from the same run:
- κ=0.5 scored 6/100 ≈ push-only: a below-threshold ring adds nothing to a peak
  detector. Detection is a CLIFF in κ, not a slope.
- Push-only at J=2 mN·s already scores 99/100: the blind→perfect transition spans
  ~one order of magnitude of impulse, inside Shishir's own 0.05–1 mN·s bracket.
- Combined with the verified side-mounted chip (κ varies with graze location):
  the same graze may be ~always detected on one side of the ball and ~never on the
  other. Geometry lottery. Candidate central claim of post 2.

Known sim caveats at round 1: single-axis model; threshold detector (real system
may matched-filter or use gyro); κ=180 Hz ring frequency assumed; noise σ=1 m/s²
assumed; fig_traces draws the threshold on the raw trace (wrong signal — teaching
moment, fix in round 2 figures).

Flaw resolution (2026-07-06): Shishir found it by asking "does the traces figure
already have the hpf output" — it didn't; the threshold dashes were drawn on the
raw trace while the detector thresholds the high-passed signal. Fixed: each row
now overlays the filtered signal (blue) on the raw (gray); the no-touch row is
finally self-consistent (raw roams ±3, blue sits inside the dashes), and the
κ=2 row shows the detected burst clearly while the raw trace shows nothing.
Meta-lesson for post 2: the broadcast heartbeat graphic commits exactly this sin —
showing a raw-looking wiggle while the decision happens in a domain nobody sees.

## Round 2 — 2026-07-06: "where does the κ=2 cliff sit in J?"

Shishir predicted: 0.2 mN·s. Sim result: ~0.35 mN·s (TPR: 0.01 at J≤0.2, 0.21 at
0.3, 0.80 at 0.4, 1.00 at 0.5+; threshold 0.311 m/s² at 1% FPR). Off by 1.75× on a
20×-wide bracket — well calibrated. Notable: at his guessed 0.2 the detector is
still fully BLIND (TPR = FPR floor), not half-working: cliffs don't give partial
credit.

Threshold-sensitivity check: 10× stricter false alarms (0.1%, threshold 0.380)
moves the cliff only ~0.35 → ~0.45 mN·s. Steep noise tails make false-alarm
protection cheap; nothing buys detection below the noise ceiling.

Closed-form account (all Shishir-derived quantities): cliff = noise ceiling ÷ ring
gain = 0.31 m/s² ÷ (κ · πJ/2mτ · anti-alias factor ≈ 1.0 m/s² per mN·s) ≈ 0.3.

Post-2 synthesis: the graze bracket 0.05–1 mN·s STRADDLES the cliff. A few-hairs
whisper is undetectable even with a loud ring; a firm brush is certain. The
heartbeat spike therefore means: firmer-than-gentlest touch, OR a smarter detector
than our threshold model, OR a rare false alarm — undecidable without the
unpublished thresholds. Caveats: κ=2, 180 Hz ring, σ=1 m/s², single axis (cliff
location moves with these; cliff existence doesn't).

## Round 3 — 2026-07-07: the twist (gyro channel), from Shishir's own question

Channel discovered by Shishir asking "wouldn't the gyro also be in play?" Socratic
chain: air shoves but can't twist (Q1-Q2) → force decomposition, tangential feeds
torque (his insight) → Δω ceiling 1.8°/s = 0.06% of baseline spin, 5× the push's
fractional effect (Q3, his arithmetic after two unit gremlins) → single-reading
SNR ≈ 12 (Q4a) → two-window mean-comparison detector (his design, Q4b) → Allan-U
window limits: bias drift + non-stationary spin (Q5, both named by him).

Envelope 1 (detector as designed): BLIND at all J — the aero spin-decay slides the
baseline ~2.9°/s between windows, parking the null statistic above any step; a real
graze partially CANCELS the slide (anti-correlated detector). His Q5(ii) enemy,
live on the bench.

Fix (his design, Q6b): fit line to before-window, extrapolate, subtract, re-compare.

Envelope 2: Shishir predicted cliff at 0.07 mN·s ("5× lower than shudder's 0.35,
mirroring the 5× stronger signal"). Result: detrended threshold 0.389°/s (13× the
jitter-only ideal — the Allan tax priced in); cliff at f=1 ≈ 0.23 mN·s, at f=0.3
≈ 0.7. Verdict: direction right (twist beats shudder, best case), magnitude 3×
optimistic. Pattern across rounds: direction right, bullish on effect size.

Key findings: (1) every channel carries one unmeasured coupling that decides its
fate — shudder has κ, twist has f; (2) κ and f are independent → fusion hedges the
geometry lottery; (3) the twist has engineering headroom (better gyro/drift model
moves the cliff), the shudder doesn't.

## Terminology note (2026-07-08)

Post 1 unified the per-channel couplings under subscripted kappas: κ_push
(perpendicular force share), κ_shudder (shell-transmission gain; called plain
"κ" in rounds 1-2 above), κ_twist (tangential/grip share; called "f" or
"f_split" in round 3 above). Code renamed to match (kappa_shudder,
kappa_twist). The three are independent draws — the basis of the fusion
argument for post 2.

## Round 4 — 2026-07-08: verdict stability and the beep/silence asymmetry

Socratic session post-publish (recap quiz first: channels/rules solid, κ
definitions drifted and were re-anchored). Two derived quantities, both
Shishir-computed:

1. Verdict disagreement: same graze, two matches, independent noise →
   P(disagree) = 2p(1−p), peaking at 50% where the detectability curve
   crosses p = 0.5. Cliff-vs-slope debate resolved: a gentle slope doesn't
   buy reliability, it widens the coin-flip zone. Cliffs confine it.
   Sim deliverable for post 2: width of the band where 2p(1−p) exceeds
   tolerance, per channel (twist's zone is visibly wider than shudder's —
   see fig_twist_detectability.png, ~3× in J vs the shudder's snap).
2. Likelihood-ratio asymmetry at the 50% point, FPR 1%: beep → LR 50
   toward touch; silence → LR ~2 toward no-touch. Convicting on a beep is
   defensible; exonerating on silence is not. The broadcast graphic only
   ever shows the beep case.

Planted flag (post 4): Shishir phrased the beep as "50× more likely there's
a touch" — LR/posterior conflation, deliberately left open. Needs prior
odds of a graze per flight → hierarchical Bayes post.

## Round 5 — 2026-07-08: cliffs under audit-corrected inputs

Inputs corrected per research/assumption-audit.md: ride band 80→20 Hz, ride
amplitude ×0.65 (drag 2→1.3 N), gyro white jitter 0.15→0.06 dps (drift
unchanged). Shishir waived predictions this round ("just proceed").

Results (fig_round5_audit.png):
- Shudder (κ=2): J50 0.346 → 0.246 mN·s (−29%); 10→90% width ×1.84 → ×1.60.
- Twist (κ_twist=1, detrended): J50 0.213 → 0.188 mN·s (−12%); width ~×3 both.

Findings:
1. Post 1's "early insight" SURVIVES: both transitions stay abrupt (shudder
   even steeper). Cliff existence is structural; only locations moved. No
   post-1 edit needed for that line.
2. TWIST SURPRISE: white jitter dropped 2.5× but the cliff moved only 12%.
   The detrended detector's floor is dominated by bias drift (random walk),
   which the audit left unchanged — the Allan tax is the binding constraint,
   not the chip's white noise. Sharpens round 3's finding: a quieter gyro
   buys almost nothing; a better drift model is the engineering headroom.
3. Shudder moved less than the noise reduction naively suggests: with the
   aero band at 20 Hz, almost nothing aero leaks past the 100 Hz filter —
   the new floor is the accelerometer's own white noise (SIG_SENSOR), i.e.,
   the shudder channel is now sensor-limited, not aero-limited.

Decision: sim defaults stay at post-1 values for reproducibility of rounds
1–4; corrected values become the post-2 baseline when the psychometric-fit
refactor lands.

## Round 6 — 2026-07-11: psychometric fit (logistic in log-J, 1% floor)

First round on the audit-corrected inputs (post-2 baseline per the round-5
decision). Model: p(J) = 0.01 + 0.99·sigmoid(s·(log J − log J50)), binomial
MLE (numpy zooming grid search — no scipy in the venv), parametric bootstrap
CI cross-checked against a profile-likelihood CI. Twist: the 11-value ×1.4
grid × 400 trials; shudder: the round-5 15-point grid × 400.

SEALED ENVELOPE — 95% CI half-width (±%) on fitted J50, twist κ_twist = 1,
detrended. Shishir predicted ±0.3–0.4% ("tighter by a factor of 10" than his
single-point ±3–4% dot-noise derivation). Result: **±3.3%** (bootstrap;
profile agrees, ±3.2%). Verdict: direction right — pooling does tighten —
but ~10× optimistic on the size of the gain. Round-3 pattern holds.

Fitted values (corrected inputs):
- Twist: J50 = 0.176 mN·s, 95% CI [0.171, 0.182]; steepness s = 3.86
  [3.57, 4.19] → 10→90% width ×3.12. Six points sit mid-transition
  (counts 10/25/62/119/225/394 of 400) — the grid resolves this slope.
- Shudder: J50 = 0.270 mN·s; s = 30.4 → width ×1.16. Exactly ONE point
  mid-transition (283/400); bootstrap CI ±0.1% vs profile ±2.3% — the two
  methods disagree 20× here and agree on the twist.

Open threads (worked socratically; findings appended when resolved):
1. Where did the predicted factor 10 go? RESOLVED 2026-07-13 — see below.
2. Why do bootstrap and profile agree on the twist and split 20× on the
   shudder — and which one do you trust? RESOLVED 2026-07-13 — see below.
3. Fitted twist J50 0.176 sits ~7% below round 5's crossing estimate 0.188 —
   outside the new CI. Something the CI doesn't cover moved. (pending)

Figure: figs/fig_round6_fit.png.

### Thread 1 resolution — 2026-07-13, revision arc (rungs a–e)

Shishir asked for a from-scratch rebuild of the CI chain ("start fresh on
sims, step by step"); rungs (a) one dot = 400 flights counted, (b) binomial
wobble, were solid; revision ran (c) onward. All numbers his:

- Rung (c): dot at J=0.20 reads 0.56; wobble √(0.56·0.44/400) = ±2.5 POINTS
  (absolute — the relative-vs-absolute currency slip was caught and fixed en
  route, same family as round 3's unit gremlins); local grade from the
  straddling dots = 26 pp over a 33% rise ≈ 0.8 pp per 1% of J; slide of the
  50% crossing = 2.5/0.8 ≈ ±3.1% at 1σ. Reproduces his week-old ±3–4%.
- Rung (d): six ramp dots pooled → ±3.1/√6 ≈ ±1.2%. Pooling pays in √N.
- Rung (e): ×~2 for a 95% quote → ±2.4%, vs the sim's ±3.3%. Leftover gap =
  unequal witnesses (edge-of-ramp dots are blunter; effective N < 6) + the
  steepness knob being fit from the same data.

The factor-10 autopsy, his closing computation: delivering his sealed
±0.31% as a 95% CI requires 3.1·2/√N = 0.31 → N ≈ 400 equally sharp ramp
dots (160,000 ramp flights) vs the 6 dots (2,400) actually run. A 10×
tighter CI costs ~100× the informative data; the residual ×2 was the
1σ-vs-95% quote. Meta-note for the pacing thread: round 6 originally landed
fit + bootstrap + profile in one delivery — too many new ideas per step;
the rung-by-rung rebuild is the corrective pattern.

### Thread 2 resolution — 2026-07-13 (worked socratically)

Shishir's chain: one ramp dot can't set the slope alone → he pushed back
that the flanking floor/ceiling dots DO carry slope information (correct;
sharpened to: they bound steepness from below — the rise must fit inside
the ×1.9 gap — but nothing punishes an arbitrarily steep cliff, so no
upper bound) → high slope uncertainty means J50 slides along a ridge of
(J50, s) pairs that all match the single mid-dot (his words: "depending on
what the slope is, the J50 number could vary significantly") → bootstrap
±0.1% fails the sniff test → steepness knob absorbs each replay's mid-dot
wobble (after one terminology stumble on "absorbing" — relocated, not
reduced).

Mechanism: the parametric bootstrap crowns the fitted curve as truth and
measures only the replay scatter the refits FAIL to absorb. On a ridge the
free knob (s) drains all of it — smoking gun: the bootstrap's s-interval
[24.5, 37.4] (±21%) is the mid-dot's binomial wobble laundered through the
s knob, while J50 stays glued (±0.1%). Reproducibility ≠ identifiability.
The profile likelihood crowns no one — it sweeps the whole unruled-out
family → honest ±2.3%. Twist: six witnesses leave no free knob; both
methods agree; agreement-vs-split of the two CI methods is itself the
diagnostic (post-2 keeper).

Honesty note: the fitted shudder steepness s = 30.4 is search-budget-
limited, not measured — the likelihood creeps monotonically toward an
infinitely steep step glued to the mid-dot; the optimizer's patience wears
the number. Same caveat applies to the drawn curve in fig_round6_fit.png
(right panel): the cliff's steepness there is illustrative.

Consequence for sequencing: adaptive sampling moves AHEAD of the
disagreement-zone overlay — the shudder's disagreement-zone width needs an
identified steepness first, which the ×1.4 grid cannot deliver.

## Round 7 — 2026-07-13: the staircase (adaptive sampling, shudder)

Design (Shishir's): blind 15-point seed grid (6,000 flights), then six waves
of 1,000; before each wave refit on ALL accumulated data, draw the surviving
family (joint-95% likelihood region — "the fan"), place the wave 5×200 where
the fan is widest. His criterion, refined en route: not sparsity — "sparsity
+ how fast the change is," made robust as "where the surviving curves
disagree most."

SEALED ENVELOPE: final 95% profile CI half-width on shudder J50 after 12k
flights (was ±2.3–2.4% on the blind 6k). Shishir predicted ±1.62%, reasoning
2.3/√2 — √N applied to total flights. Side bet: does steepness get a finite
upper bound — YES, hedged ("steepness is so high I wouldn't be surprised if
No").

Results (fig_round7_staircase.png):

| wave | flights | profile CI on J50 |
|---|---|---|
| 0 (blind) | 6,000 | ±2.40% |
| 1 | 7,000 | ±0.25% |
| 2 | 8,000 | ±0.20% |
| 3 | 9,000 | ±0.15% |
| 4–6 | 10–12,000 | ±0.10% |

Final: J50 = 0.2721 mN·s, profile ±0.10%, bootstrap ±0.16% — the two
methods RECONCILE once the ridge is broken (the round-6 diagnostic confirmed
in both directions). Steepness profile [40.6, 43.5] — bounded, finite,
enormous (10→90% width ×1.11: the shudder cliff is genuinely near-vertical).

Score: prediction ±1.62% vs actual ±0.10% — off 16×, and for the FIRST time
in the log the miss is PESSIMISTIC. Side bet: primary call (yes) correct;
hedge unnecessary. Narrative keeper: his round-6 sealed prediction (±0.35%)
was wrong for the blind experiment but is almost exactly what the adaptive
experiment delivers — he predicted the smart experiment's precision, one
round early, for the wrong design.

Open thread 4: why did √N-on-total-flights fail here, in the pessimistic
direction — what did wave 1's 1,000 flights have that the seed's 6,000
didn't? RESOLVED 2026-07-13:

Shishir's diagnosis: wave 1 carried "more structural signal" — the flight
distributions aren't equivalent, √N presumes exchangeable contributions.
Sharpened in two steps: (1) the binding condition isn't gaussianity (his
guess) but equal INFORMATION per flight — flats contribute ~zero, ramp
flights contribute ∝ grade²; √N is bookkeeping for equal contributions.
(2) Wave 1's 10× decomposes as ~1.9× honest √N (ramp flights 400→1,400)
times ~5× REGIME CHANGE: dots at several ramp heights gave steepness its
second witness and killed the ridge — identifiability isn't bought in
increments. Confirmation: post-ridge, √N resumed on ramp-flight count
(waves 2–6: predicted 2.1×, observed 2.5×). His envelope math was right
one regime too late, applied to the wrong N.
