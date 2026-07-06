# Cricket DRS — research findings (agent: cricket-drs, 2026-07-05)

## Umpire's Call (ball-tracking, LBW)
- Core rule: original on-field decision stands unless tracking shows MORE than 50% of
  the ball in the required zone; 1–50% = "Umpire's Call", original stands.
  (Wikipedia DRS, corroborated ocbsports.com — secondary.)
- Auto-Umpire's-Call triggers encode ERROR PROPAGATION in the playing conditions:
  impact ≥300 cm from stumps, or <40 cm between pitching and impact points →
  prediction uncertainty compounds with projection distance, so the protocol widens
  the deference zone. (Secondary paraphrase of ICC playing conditions; ICC's own PDF
  not obtained — flag before quoting verbatim.)
- Stated rationale: a designed uncertainty buffer ("doubts in the accuracy of the
  technology"), not a proximity judgment.
- 2021: Wickets Zone raised to top of stumps to equalize height vs width margins.
- Hawk-Eye's founder on record: no need for Umpire's Call "if starting from scratch"
  (Wisden interview) — vendor sees it as a legacy uncertainty compromise.
  https://www.wisden.com/series/england-in-india-2023-24/cricket-news/hawkeye-inventor-no-need-for-umpires-call-if-starting-from-scratch

## Error margins
- mm figures inconsistent (3.6 / 5 / 2.2 mm) with no primary doc traced; Wikipedia's
  "90% accuracy" is unsourced. Present as "commonly reported range" only. LOW confidence.
- ICC commissioned independent testing (Cambridge-based, Computer Vision Consulting
  Ltd; Hawk-Eye vs Virtual Eye vs ground truth) — espncricinfo.com/story/553449
  (403'd, via snippet). Exact figures unverified.

## Snicko / UltraEdge
- Mechanism: stump-mic audio synced to high-speed video; spike-coincidence = edge.
  Real-Time Snicko enables in-review use. UltraEdge (Sony): directional mics + filtering.
- Known false-positive sources (named consistently): bat-on-pad, ball brushing
  clothing. UltraEdge explicitly cannot always distinguish bat vs pad — why Hot Spot
  + replay run alongside. No primary validation study located.
- Hot Spot: players used silicone tape to suppress thermal edge signatures; "MIT
  report" confirming this is cited by Wikipedia but UNVERIFIED (no title/author/venue
  found) — do not cite as MIT without more digging.

## Studies / statements
- Sinha, Pandey & Singh (2017), IJSER 8, pp 60-62: 26% of player reviews overturned
  (2009–2017); batting ~34%, bowling ~20% success. Real citation, low-tier journal.

## Controversies (uncertainty as the story)
- Shan Masood LBW (Pak v NZ, Dubai, Dec 2014): Hawk-Eye ADMITTED operator error →
  wrong decision. (Secondary, specific/checkable.)
- Saeed Ajmal 2011 WC semi: Hawk-Eye reportedly conceded a wrong LBW projection —
  single-sourced, verify before use.
- Zak Crawley LBW (Rajkot, Feb 2024): upheld on Umpire's Call; Stokes claimed a
  graphical error and called for Umpire's Call to be scrapped. HIGH confidence on
  event + quote; "graphical error" is Stokes's secondhand account.
  https://www.espncricinfo.com/story/ben-stokes-wants-drs-to-scrap-umpire-s-call-1421714

## Publishing flags
- mm accuracy figures: range only, no primary.
- MIT/Hot Spot report: unverified.
- IJSER paper: cite with rigor caveat.
- Umpire's Call mechanics + named controversies: consistently multi-sourced.
