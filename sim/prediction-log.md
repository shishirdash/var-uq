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
