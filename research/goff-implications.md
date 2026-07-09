# Goff, "Power and spin in the beautiful game" (Physics Today 63(7), 2010) —
# implications for the VAR-UQ project (dug 2026-07-09)

Source: https://physicstoday.aip.org/quick-study/power-and-spin-in-the-beautiful-game
Author: John Eric Goff (Lynchburg) — same Goff as the Goff & Carré trajectory
papers already in our audit. Facts used: drag crisis ~12 m/s for a football
("a medium-range pass"); van Persie kick Re 5e5 (boot) -> 3e5 (goal), initial
drag ~15% above ball weight; Cd depends on Re AND spin, varies during flight;
Magnus force on a free kick comparable to ball weight; spin ladder 600 rpm
(free kick) / 2000 (curveball) / 2500+ (golf); surface roughness moves the
crisis to lower Re (golf dimples; explains smooth-Jabulani pathology);
through-center kick = speed, off-center = spin (competing needs).

## 1. The drag crisis sits INSIDE the game's speed range
Crisis at ~12 m/s; crosses fly ~20, passes straddle it. Two consequences:

a) NON-STATIONARY RIDE WITHIN A FLIGHT. Van Persie's kick *ends* at
   Re 3e5 — the upper edge of the critical band (2.2–3.0e5 per Asai). A long
   ball decelerates INTO the crisis: Cd rises 0.14 -> ~0.4-0.5 as v falls
   through it, so the ride's amplitude/character shifts late in flight. This
   is the accelerometer-channel analog of the spin-decay slide that blinded
   the naive gyro detector (round 3). Same fix family: estimate the baseline
   from THIS flight's pre-graze window, not from a global model.
   => Unifying detection principle across channels: baselines must be
   learned per flight. (Post 2/3 theme; hierarchical Bayes hook.)

b) PER-FLIGHT FALSE-ALARM RATES. A threshold calibrated to 1% FPR on
   supercritical (fast, smooth-riding) flights delivers a DIFFERENT actual
   FPR on slow or near-crisis flights. Our sim calibrates and tests inside
   one regime — real fleets can't. "1% FPR" is a fleet average, not an
   incident guarantee. (Strengthens the disagreement-zone story, round 4.)

## 2. Ride noise depends on spin (knuckle axis)
Cd depends on spin; near-zero-spin balls knuckle (Hong & Asai: ~3.5 Hz
large-amplitude force flutter). So sigma_aero is conditional on omega:
low-spin flights are noisier in the low band exactly where our filter
leaks. Our incident ball (8 rev/s) was healthily spinning — good for the
ruling — but a knuckling cross is the worst case for any accelerometer
rule. => Sim axis to add: sigma_aero(omega). Also note: our corrected
"below ~20 Hz" band edge is spin-state-dependent.

## 3. The Magnus echo: a twist regenerates a push-sized flight deviation
New Fermi thread. Magnus on a free kick ~ ball weight (~4 N at ~34 m/s,
10 rev/s). Scaled to our cross (F_M ~ omega*v): ~2 N. A graze's spin change
(Delta-omega/omega up to 6.25e-4) perturbs Magnus by ~1.25 mN, acting for
the remaining ~0.5 s => extra impulse ~0.6 mN*s — SAME ORDER as the graze's
own direct impulse. Both scale linearly in J, so the echo is a fixed ~60%
multiplier on the tangential component's momentum effect (at this v, omega,
flight time). Extra deflection <= ~0.35 mm — still invisible to cameras, so
detectability is unchanged; but physically the channels COUPLE downstream:
twist -> Magnus -> path. The graze keeps pushing the ball after it's gone,
via the air. (Candidate post-2 aside or post-1 footnote; also a caution for
interpreting "push deflection" as the only path effect.)
Assumptions: F_M ∝ omega (small spin parameter), remaining flight 0.5 s.

## 4. Joint-sim prior structure falls out of the competing-needs argument
Kicker's dilemma (through-center = speed, off-center = spin) is our
kappa_push/kappa_twist decomposition performed on purpose. Natural joint-sim
parameterization: draw contact angle theta -> kappa_push = cos(theta),
kappa_twist = sin(theta) x slip-efficiency; kappa_shudder independent
(transmission path lottery). So: 3 kappas but only 2 independent lotteries
(geometry, transmission). Replaces the "3 independent draws" simplification
post 1 now flags. Goff's line "the air exerts only a single force on the
ball; how that force is split into components is up to the scientist" is
the quotable version of the whole kappa philosophy.

## 5. Smaller items
- Our corrected drag cross-checks against Goff's number: his 15%-above-
  weight at ~34 m/s implies Cd ~0.18; Asai's measurements give 0.13-0.15;
  at 20 m/s both put drag ~1.3-1.7 N, firmly below the original 2.28 N.
- Cd is ball-model-specific (roughness/seams set the crisis). Our 0.14 is
  Telstar-18-class; the TRIONDA's Cd is unpublished — even the audit's
  corrections carry an unpublished-number error bar. (Theme continuity.)
- Jabulani footnote can be upgraded from trivia to mechanism: smooth shell
  -> crisis at higher Re -> erratic/knuckle-prone at game speeds.
- Spin ladder (600/2000/2500 rpm) + drag-crisis-at-a-medium-pass are both
  lay-friendly footnote material (placement suggestions already drafted).

## Sim to-do (queue into post-2 workbench)
1. Per-flight baseline estimation for the accelerometer channel (mirror of
   the gyro detrend) — then re-derive the FPR story.
2. sigma_aero(omega) condition axis; knuckle worst case.
3. Joint sim with theta-decomposition prior + independent kappa_shudder.
4. Optional: within-flight Cd drift for long flights (crisis crossing).
