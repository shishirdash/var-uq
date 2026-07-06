# Connected Ball Technology — research findings (agent: ball-tech, 2026-07-05)

Confidence tags: PRIMARY (FIFA/Adidas/KINEXON/academic) · JOURNALISM · UNVERIFIED.

## Sensor hardware
- KINEXON (German firm; chip developed by co-founder Maximilian Schmidt). PRIMARY (TUM press release, Adidas newsroom).
- IMU (accel + gyro, possibly magnetometer) at 500 Hz; reports position, velocity, spin, touch state. PRIMARY (Adidas newsroom).
- UWB positioning: in KINEXON's product line, but NOT confirmed inside the match ball itself. UNVERIFIED for the in-ball unit.
- Suspension: proprietary "adidas Suspension System" at ball center. PRIMARY.
- Weight discrepancy: 3 g (bare chip, TUM/Euro-2024 = PRIMARY) vs 14 g ("the sensor", 2022 journalism = JOURNALISM). Don't quote one number without caveat.
- Power: induction-charged sealed battery; ~6 h active / ~18 d standby is JOURNALISM, unverified.
- Data path: sensor → roof antennas → KINEXON edge compute → FIFA VAR room, "within seconds", 500 Hz stream. PRIMARY (Adidas + inside.fifa.com).

## 2026 Trionda
- Same core 500 Hz KINEXON IMU. PRIMARY.
- Sensor placement — UPGRADED TO PRIMARY (2026-07-06, verified against the Adidas
  unveil release directly): "a side mounted chip system"; "The 500Hz inertial
  measurement unit (IMU) motion sensor chip now sits inside a specially created layer
  in one of the four panels." Counter-balances across the other three panels for
  flight stability. Source: news.adidas.com Trionda unveil release. Corroborated:
  FOX Sports, Man of Many, TechTimes, Dezeen coverage.
  ← Directly moves the κ prior UP (chip embedded in the shell = direct structural
  coupling for the ring; no tether attenuation). Adds a new variance term: graze on
  the chip's panel vs. the far side. Adds centripetal term: chip at radius ~0.1 m
  spinning at ~8 rev/s feels ω²r ≈ 250 m/s² quasi-DC — huge but low-frequency,
  below the high-pass; raises dynamic-range needs.
- 4-panel thermally bonded shell, lowest panel count in WC history (aero claim). JOURNALISM.
- Scientific American on Trionda geometry/physics (added 2026-07-06,
  scientificamerican.com "The surprising math and physics behind the 2026 Trionda"):
  tetrahedron-based 4-panel tiling; only 12 rotational symmetries vs 60 for the
  classic Telstar; seams/divots are deliberately tuned roughness to manage the drag
  crisis; low-spin knuckling risk; Jabulani (2010, also tetrahedron-based) as the
  too-smooth cautionary tale; physicist John Eric Goff planning wind-tunnel tests
  (no C_d figures published yet). ← Supports the noise model: orientation-dependent
  aero force at spin frequency has a geometric basis.
- No primary spec sheet comparing Trionda's sensor to predecessors. Any "faster/more granular" claim = JOURNALISM.

## Touch detection — the weak-evidence item
- Public description is only "heartbeat"/impact-signature language. NO primary source describes the algorithm (threshold vs classifier vs spectral). UNVERIFIED beyond "IMU detects an impact signature".
- NO published FP/FN rate, confidence interval, or accuracy figure anywhere. Testing claims are qualitative ("rigorously and robustly tested... blind testing" at 2021 Arab Cup / Club WC) and are about ball feel, not detection accuracy. The gap is itself the finding.
- Ronaldo/Bruno Fernandes (Portugal 3–2 Uruguay, 2022 groups): FIFA/Adidas statement: "we are able to definitively show no contact on the ball from Cristiano Ronaldo" — justified by ABSENCE of a heartbeat. No waveform, threshold, or data published; conclusion only. PRIMARY quote (via Goal/Sportskeeda distribution).
  - Note for the series: 2022 = absence of spike taken as proof of no touch; 2026 Matanović = presence of spike taken as proof of touch. Asymmetric error types (false negative vs false positive), same certainty language.

## SAOT
- 12 roof cameras; 29 tracked points per player at 50 fps. PRIMARY (inside.fifa.com).
- Ball IMU's 500 Hz kick-point timing pins "the exact first touch"; combined with camera limb tracking "using AI". PRIMARY.
- NO published numeric tolerance (± cm or ± ms) for the combined system — confirmed absence on FIFA's SAOT page.

## Academic/criticism
- No peer-reviewed metrology analysis of SAOT or the ball sensor found. Closest: CHI 2023 "Spectators of AI: Football Fans vs. the Semi-Automated Offside Technology" (dl.acm.org/doi/10.1145/3544549.3585870) — HCI/fan perception, not physics. Dead end for the metrology angle.
- Circulating criticism is qualitative: occlusion, calibration, millimeter-scale rulings vs. the rule's intent. No error-bar numbers. JOURNALISM.
- Net citable claim: real gap between confidence language ("definitively", "unmatched accuracy") and any published quantitative error rate, for both touch detection and SAOT.

## Sources
- inside.fifa.com/innovation/world-cup-2022/semi-automated-offside-technology (PRIMARY)
- news.adidas.com/football/adidas-reveals-the-first-fifa-world-cup-official-match-ball-featuring-connected-ball-technology (PRIMARY)
- TUM press release "High-tech sensors for the European Championship ball" (PRIMARY)
- kinexon-sports.com/blog/connected-ball-technology-data; kinexon.com/technology/ball-tracking (PRIMARY)
- FIFA Ronaldo/Uruguay statement via goal.com, sportskeeda.com (PRIMARY quote)
- techtimes.com Trionda sensor piece; espn.com "smart ball... remember to charge it" (JOURNALISM)
- sportbusiness.com SAOT one-year retrospective (JOURNALISM)
- dl.acm.org/doi/10.1145/3544549.3585870 (CHI 2023)
