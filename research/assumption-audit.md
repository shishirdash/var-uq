# Assumption audit — post 1 Fermi anchors vs literature (2026-07-08)

Requested by Shishir post-publish. Three research agents (human forces, ball
flight, sensors). Verdicts: SUPPORTED / PLAUSIBLE / NEEDS CORRECTION.

## Verdict table

| # | Claim in post/sim | Our number | Literature says | Verdict |
|---|---|---|---|---|
| 1 | IMU report rate | 500 Hz | 500 Hz, 16-bit (Adidas/KINEXON, multiple independent trade sources) | SUPPORTED |
| 2 | Ball mass / radius | 410–450 g, r ≈ 11 cm | IFAB Law 2: 410–450 g, circumference 68–70 cm → r ≈ 10.8–11.1 cm | SUPPORTED |
| 3 | Moment of inertia | ⅔mr² (thin shell) | Standard first-order model for a football; minor seam/valve asymmetry | SUPPORTED |
| 4 | Cross flight speed | ~20 m/s | Kicks span ~15–35 m/s; crosses mid-range; defensible estimate, no direct "cross speed" study | PLAUSIBLE |
| 5 | Spin rate | ~8 rev/s | Good free kicks ~600 rpm (10 rev/s); Ronaldo-style ~5; 8 in observed range, upper end | SUPPORTED |
| 6 | Graze contact time | ~5 ms | Full header ~12 ms (peak ~6 ms); kick 8–10 ms; graze shorter than square hit — right direction | SUPPORTED |
| 7 | Spin decay | ~1 %/s, "tens of seconds" | Measured ~2–3 %/s early flight (5.8→5.7 rev/s over 0.8 s); ours slightly conservative | SUPPORTED |
| 8 | Elevator button force | ~1 N | Real elevator/push buttons actuate at **2.5–5 N** (MIL-STD-1472F, panel patents); ~0.5–0.8 N is a light *keyboard key* | NEEDS CORRECTION |
| 9 | Hair-graze force | 0.01–0.2 N | Unmeasured anywhere. Single fiber bends at µN–mN; our bracket = "small tuft against scalp," plausible, uncitable | PLAUSIBLE (declared estimate) |
| 10 | Drag coefficient | C_d ≈ 0.25 → ~2 N at 20 m/s | At 20 m/s, Re ≈ 2.9×10⁵ = supercritical; measured C_d **0.13–0.15** (Asai, Goff) → **~1.3 N** | NEEDS CORRECTION |
| 11 | Turbulence band | "below ~80 Hz" | Measured unsteady aero on soccer balls: dominant oscillation **~3.5 Hz** (Hong & Asai); Strouhal estimate ~18 Hz. Real band: single digits to ~20 Hz | NEEDS CORRECTION (we overstated ~4×) |
| 12 | Gyro jitter | ±0.1–0.2 °/s per reading | Modern chip class in the ball (ICM-42688-P-like): 2.8 mdps/√Hz → **~0.04–0.08 °/s RMS** at 250 Hz BW. Ours 2–5× pessimistic | NEEDS CORRECTION (conservative direction) |
| 13 | Bias drift / Allan framing | drift caps averaging window | IEEE-952 standard tool; consumer bias instability ~10–30 °/hr. Mechanism correctly described | SUPPORTED |
| 14 | Shudder frequency | ~180 Hz (sim), "hundreds of Hz" (post) | No soccer-ball modal study public. Basketball: shell mode ~410 Hz, breathing ~900 Hz (Russell/PSU); soccer larger/softer → lower. "Few hundred Hz" fine; 180 Hz is a placeholder | PLAUSIBLE (declared estimate) |
| 15 | Gyro range vs 2880 °/s spin (audit question, not a post claim) | — | Ball's gyro rated **±4000 °/s** (SensorTips et al.) — 8 rev/s sits at 72% FS, no saturation; engineers over-ranged deliberately. 16-bit LSB ≈ 0.12 °/s | RESOLVED (good news) |

## Downstream implications

**Post 1 body/footnotes:**
- Swap the 1 N anchor: either "pressing a keyboard key is roughly half a newton"
  (keeps the hundredth-to-a-fifth bracket derivation in the same decade) or keep
  elevator buttons at their real 2.5–5 N and rescale the fraction.
- Footnote 4.1: C_d ≈ 0.25 → ~0.14 (supercritical), drag ~2 N → ~1.3 N.
- Turbulence "below ~80 Hz" (body + footnote 4.2) → "below ~20 Hz". Note this
  WIDENS the ride/shudder frequency gap — the detection rule gets more
  comfortable, not less. 100 Hz filter unchanged.
- Gyro tremble ±0.1–0.2 °/s → "±0.05–0.15" or keep with a "conservative" flag.
- Shudder "hundreds of Hz" fine as is; could cite basketball modal analogy.

**Sim inputs (post 2 material — run as predict-then-check round 5):**
- GYRO_JITTER_DPS 0.15 → ~0.06 (moves twist cliff DOWN — predict how far first)
- noise band edge 80 → ~20 Hz (moves shudder cliff DOWN; ride quieter above filter)
- drag/ride magnitude smaller → push-vs-ride ratio shifts but push stays dead
- shudder 180 Hz: keep, declared placeholder; kitchen IMU experiment is the
  ground-truth path (post 5)

## Sources

Ball flight: Asai et al., Fundamental aerodynamics of the soccer ball (Sports
Eng.); Goff & Carré EJP 2010; Hong & Asai, unsteady aero on a knuckle ball
(Procedia Eng.); Spin Decay of Sports Balls in Flight (P172); IFAB Laws of the
Game, Law 2; Physics Today, Power and spin in the beautiful game.

Human forces: MIL-STD-1472F push-button ranges (GTRI HSIMed); elevator panel
patent US7404470 (2.5–5 N); Univ. Michigan keypress-force study; Swift 1995 +
ScienceDirect 2022 hair bending stiffness; Purdue heading biomechanics;
kicking-biomechanics review.

Sensors: Adidas connected-ball press release; SensorTips "How sensors help you
play ball, pt. 2" (500 Hz, ±4000 dps gyro); ICM-42688-P datasheet (TDK
InvenSense, 2.8 mdps/√Hz); ADI EngineerZone on in-run bias stability; Wrona,
Gyro Noise and Allan Deviation; Russell (Penn State), Basketballs as Spherical
Acoustic Cavities; Springer Sports Eng. soccer-ball SLDV modal paper (paywalled,
methodology only).

## Addendum (2026-07-09)

Keyboard actuation force primary source located and verified: RESNA 2004
proceedings page quoting Martin et al. (U. Michigan) minimum key actuation
make-force 0.47 N and Rose (1991) recommended 0.50 N activation force.
https://www.resna.org/sites/default/files/legacy/conference/proceedings/2004/Papers/StudentDesign/OUT/KeyboardForce.html
Post 1 now inline-links all four corrected numbers + Law 2 + spin decay +
turbulence band + gyro datasheet, and the sources footer links this audit.

Flight-speed source added (2026-07-09): peer-reviewed instep-kick review
(PMC3786235) reports maximal-kick ball speeds 18-35 m/s (pros ~30, elite
women ~21.5, 1990 World Cup match play 32-35). A cross is submaximal, so
~20 m/s sits low-middle of the measured range. Verdict upgraded
PLAUSIBLE -> SUPPORTED; linked inline in post 1.
https://pmc.ncbi.nlm.nih.gov/articles/PMC3786235/

Second sweep (2026-07-09, Shishir caught the miss): shudder frequency now
declared as an estimate IN the post with the basketball modal anchor linked
(Russell/PSU, ~400-900 Hz shell/breathing modes); spin-wobble ~8 Hz linked
to Physics Today free-kick spin benchmarks. Remaining deliberately unlinked:
hair-force bracket (uncitable, declared), 11 cm lever arm (derived from the
already-linked Law 2 circumference), push-vs-ride ratio (our own derivation).
