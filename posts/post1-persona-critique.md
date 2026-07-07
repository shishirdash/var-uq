# Revision brief: 'On offsides and uncertainty' (post 1, pre-publish)

Source: the private Notion draft as of 2026-07-07 (snapshot: post1-refined-draft.md).
Panel: six parallel critics plus an editor pass. Personas per the author's spec:
a mentor-expert ML blogger, a peer AS director, a lay outsider, an AI-thought-leader,
a soccer-fan colleague panel (grounded in the real #ttworldcupbracket channel), and
a fact-checker run against the project's own sourced research notes. Finding IDs are
stable anchors for inline conversation.

## What this is trying to do

The post narrates the disallowed Croatia goal, explains the offside rule pivot and
the ball sensor, walks a Fermi analysis of what the chip can physically feel, and
lands on the absence of published error rates. A closing section describes the
AI-collaborative, socratic method used to build it. It is the debut post of the
rebranded blog ('Socratic Parroting') and the first of a planned series.

## Consensus signals worth knowing first

- Every technical critic independently called the prediction-scoring passage (1 vs 8,
  0.2 vs 0.35) the most credible thing in the post.
- Two experts chose the same line to quote: 'A sampling rate is a confession of what
  its designers wanted to see.'
- The soccer panel is unanimous on what the first channel reply will be: a dunk on
  'last pass' and 'adjudged by VAR', before anyone praises the physics.
- One genuine split (F13): the mentor wants the workshop notes cut by two-thirds;
  the AI-thought-leader wants them promoted to the lede. This is the one decision
  only the author can make.

## What is genuinely good (keep)

- K1. The close: 'Same graze, different spot on the ball, different verdict. I think
  about that more than I'd like to.' The lay reader chose it as his quote. Keep.
- K2. 'A sampling rate is a confession of what its designers wanted to see.' Double
  expert endorsement. Keep verbatim.
- K3. Plain-English glosses: accelerometer 'feels jolts', gyroscope 'feels rotation'.
  The lay reader asked for more of exactly this. Keep the pattern.
- K4. The 2022-vs-2026 asymmetry paragraph ('two different error types, no error bars
  either time'). The fan panel pastes it into Slack. Keep.
- K5. The honest misses in workshop notes. Wherever that section lands (F13), the
  scoring stays.
- K6. The refinement round improved the piece: declarative headings, added images,
  personal hedges ('I assume', 'I vaguely thought'). The voice is now clearly yours.

## Findings: tier 1 (fix before publish)

- F1. Soccer law, the headline error. Locator: heading 'The decision hinged on who
  played the last pass' and 'the graze becomes the new "last played" moment'.
  Offside is judged when the ball is last touched OR played by a teammate. A graze
  is a touch, not a pass. Fans catch this in five seconds. Fix: retitle to '...on
  when the ball was last touched'; swap 'last played' language to 'last touch'.
- F2. 'adjudged offside by VAR'. VAR and semi-automated offside recommend; the
  referee decides. Fix: 'flagged by the semi-automated system and upheld by the
  referee'.
- F3. '430 grams, per regulation'. The regulation sets a range (410 to 450 g), not a
  value. As written it commits the false-precision sin the post indicts. Fix:
  'about 430 grams (regulation allows 410-450)'.
- F4. 'The Jabulani was a weird "snipped-off" version of the Tetrahedron'. No source
  supports 'snipped-off'. Fix: 'The 2010 Jabulani was also tetrahedron-based, and
  infamously too smooth: the cautionary tale.'
- F5. 'I can generally "one-shot" create some animations'. The single most
  screenshotable line, and the workshop notes contradict it (multiple nitpick
  rounds, a caught bug). The peer-director critic: cut 'one-shot', say 'quickly
  draft', let the notes carry the honest texture.
- F6. 'the detector nearly designs itself... with almost no degrees of freedom'.
  The mentor critic: this is the confidence claim the post criticizes FIFA for.
  You derived that a high-pass filter is sensible, not that the real detector is
  one. Fix: 'a naive detector suggests itself', plus one clause conceding real
  systems add fusion, adaptive thresholds, template matching.

## Findings: tier 2 (should fix)

- F7. Sim-derived numbers read as established physics. Locator: the push/ring
  figures (0.1-2 mm/s, 50 microns, below 80 Hz, 8 cycles/s). The footer discloses;
  the body does not. Fix: one inline hedge ('on our idealized single-axis model').
  Related (mentor): the 20x-wide bracket IS the finding; own it in the sentence
  rather than letting it read as precision.
- F8. Snicko never resolved. The lay reader needs snicko defined in one clause
  ('the audio trace cricket uses to catch faint edges'). The fan panel wants the
  loop closed: the TV heartbeat is the IMU trace, not acoustic snicko. Bonus
  material: your own match-night Slack line ('I'm not sure the ref has access to
  that?') is the origin document of this post and could seed this paragraph.
- F9. False-positive rate lacks a denominator (per touch? per decision?). One
  clause fixes it (peer critic).
- F10. 'the same instrument being read with total confidence in both directions'.
  You are inferring internal confidence from press releases. Fix: 'the public
  framing asserts total confidence in both directions'.
- F11. Spoiler management: 'my honest Fermi range... straddles that cliff' gives
  away post 2's landing. Mentor's advice: tease the cliff, withhold where your
  estimate falls.
- F12. 'the ball had grazed Matanović's head'. The post itself says no replay
  showed contact. Fix: 'the touch attributed to Matanović'.

## Findings: tier 3 (structure and author's calls)

- F13. THE decision: workshop notes placement. Mentor: cut to a third; the scoring
  anecdote alone earns its place. Thought-leader: it is the lede; promote it, name
  the pattern ('socratic in both directions'), show one verbatim exchange, state
  time invested. Editor recommendation: keep post 1 physics-first and trim the
  notes here, then give the method its own dedicated post (the blog is literally
  named for it); park the thought-leader's asks (verbatim exchange, the literal
  flaw-catching question, hours spent) for that post.
- F14. The seven-bullet question list reads as a syllabus to the lay reader; he
  nearly bailed there. Fix: keep the three strongest, fold the rest into prose or
  a toggle.
- F15. The numbered arithmetic section is where the lay reader skimmed and the
  experts leaned in. Tension, not error. Softest fix: keep the derivation but
  repair the prose fragments inside it, and keep the analogies ('whisper in a
  storm') doing the narrative work.
- F16. Emotional callback: the post opens 'gutted' and ends in an ROC curve. The
  fan panel wants one closing sentence that returns to the feeling. Cheap, real.
- F17. Undefined jargon at the edges (lay reader): 'Fable' (name the model or just
  say 'a frontier model'), 'ROC curve' in the closing teaser, 'Monte Carlo'.
  One-clause glosses or cuts.
- F18. Copy nits (editor pass): the two channels are both numbered '1.' (the
  interposed paragraph breaks the list); italics glitch in '*inertial measurement
  unit. *It'; 'back-of-the-hand physics' (envelope?); 'its not noticeable'
  (apostrophe); 'Since a football isn't a rigid billiard ball.' (fragment); title
  says 'offsides' where purists write 'offside' (your call); the waveform
  screenshot needs a caption and broadcast credit; trailing space in the Notion
  page title.

## Top 3 changes if we could pick

1. Fix the soccer-law language (F1 + F2). It is the first reply your colleagues
   will write otherwise.
2. Kill 'one-shot' and hedge 'designs itself' (F5 + F6). The two screenshot-bait
   lines, flagged independently by both expert critics.
3. Decide F13, with a recommendation: trim the notes here, promise the method post.
   That satisfies the mentor now and the thought-leader later.
