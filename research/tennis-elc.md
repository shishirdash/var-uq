# Tennis electronic line calling — research findings (agent: tennis-elc, 2026-07-05)

## Accuracy figures — conflicting, no single clean number
- 2.6 mm mean error, ±0.9 mm uncertainty: ITF's own certification testing (ball cannon ~30–40 m/s at ~30°, high-speed reference camera as ground truth). itftennis.com/media/7365/elc-evaluation-paper-revision-26.pdf. PRIMARY, but figure obtained via secondary summary (PDF didn't extract) — confirm exact wording before quoting ±0.9.
- 3.6 mm: legacy figure attributed to Hawk-Eye's own site via Wikipedia. SECONDARY, treat as "commonly cited legacy figure".
- 2.2 mm: newer Hawk-Eye claim in journalism (Yahoo). UNVERIFIED.
- Honest framing: "ITF's certification testing found ~2.6 mm mean error; Hawk-Eye has claimed figures from 2.2 to 3.6 mm depending on era/system."
- Mechanics: ~10 cameras/court, triangulation, trajectory model predicts bounce point (Wikipedia, consistent across sources). "Ball skid/compression modeling" as a named step: NOT FOUND — don't use that terminology.
- Binary display, no uncertainty shown: confirmed (and is the premise of the academic critique).

## Collins & Evans — verified citation
- Harry Collins & Robert Evans, "You cannot be serious! Public understanding of technology with special reference to 'Hawk-Eye'", Public Understanding of Science 17(3), 2008, pp. 283–308. DOI: 10.1177/0963662508093370. PRIMARY (SAGE page confirmed).
- Argument: virtual reconstructions read as "exactly what happened" rather than probabilistic estimates; viewers overestimate the tech because measurement error isn't salient. They explicitly propose showing confidence intervals + "health warnings", and posed 18 open technical questions to Hawk-Eye.
- Hawk-Eye response: real exchange (open letter, Hawkins reply) documented on Collins's Cardiff page (sites.cardiff.ac.uk/harrycollins/welcome-to-the-hawk-eye-page/) — primary-adjacent, Collins's framing. Hawkins quotes via phys.org/EurekAlert: "We are not saying we get every single one right...", exact contact point "slightly subjective", "no system could achieve 0mm"; also dismissed questioning as "simply poor journalism". JOURNALISM for quotes.

## Full ELC adoption
- ATP: announced Apr 2023, ELC replaces line judges at all ATP events from 2025 incl. clay. Via cached summary of atptour.com release (403 on direct fetch); corroborated ESPN/NBC.
- Wimbledon 2025: first time in 148 years without line judges (~300 → ~80 retained as standby "match assistants"). AELTC's Sally Bolton: "maximum accuracy in our officiating". CNN. Well-corroborated JOURNALISM.
- Roland-Garros: only Slam still using human line judges (clay shows physical ball marks). JOURNALISM, single source — recheck if load-bearing.

## Wimbledon 2025 incidents — verified
- Pavlyuchenkova vs Kartal (R4): three balls not called out because a Hawk-Eye operator had accidentally deactivated ball tracking (human error, not sensor failure). AELTC then removed operators' ability to deactivate tracking. CNN.
- Fritz vs Khachanov (QF): spurious mid-point "fault" call — system didn't register the point had started (ball boy still crossing net). Raducanu and Draper publicly voiced distrust. CNN/Sky.

## ITF certification program
- Real accuracy certification: Gold/Silver/Bronze tiers (accuracy, reliability, practicality, suitability). itftennis.com/en/about-us/tennis-tech/classified-elc-systems/. PRIMARY. New tiered system July 2025 (ESPN/KFGO).

## Needs second pass before publishing
- 2.2 mm figure (no primary source)
- "skid/compression modeling" terminology (likely wrong)
- exact ITF ±0.9 mm wording (PDF unread)
- ATP 2023 release text (403, cached summary only)
