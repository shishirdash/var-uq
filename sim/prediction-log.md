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
