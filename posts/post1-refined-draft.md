# On offsides and uncertainty

(Snapshot of the refined private Notion draft, 2026-07-07. Images replaced with
[IMAGE] markers. Author's exact wording preserved, including any glitches.)

I was gutted by Croatia's disallowed last-gasp equalizer against Portugal in their
World Cup 2026 round-of-32 clash. With possibly the last kick of the game, Gvardiol
had buried an equalizer, but was adjudged offside by VAR. It felt like technology —
true to form — had sucked all the joy out of an incredible moment.

As someone who grew up on cricket's Decision Review System (DRS), I was surprised to
see the replays lean on "snicko". A heartbeat-style waveform was shown on TV as proof
that the ball had grazed Matanović's head on its way through the box. Nothing in the
super slow-mos showed any change in the ball's flight or spin, so I assume "snicko"
was the deciding factor.

[IMAGE 1: broadcast screenshot — the heartbeat waveform graphic shown on TV]

That made me think of uncertainty quantification (UQ) questions, e.g.,

- What precisely was that waveform indicating? (I vaguely thought it was "sound",
  anchoring to cricket)
- How wide are its "error bars"? (What would error bars even mean here?)
- What contributes to noise inside a flying, spinning football?
- How is the sensor physically set up, and how does that help it hear a touch?
- Does the uncertainty compound — is the offside line *itself* a measurement with its
  own error that stacks on top of the touch detection?
- What about physical unknowns: air turbulence, spin, the strength and angle of the
  bump, the speed of the ball, the leap of the player?
- And how do other sports handle this? Cricket's DRS is pretty uncontroversial, and
  it has an explicit protocol — "umpire's call" — for situations which are within
  error. Is something like that possible here? Necessary?

At work, I've been trying a sort of Q&A approach to learning new things with Claude
Code. I thought this could be a good subject for a similar approach. With Fable this
has been especially fun, since I can generally "one-shot" create some animations, or
setup holistic simulations to test my understanding.

[EMBED: interactive schematic — the play, the sensor inside the ball, and the two
detection channels. Also at shishirdash.github.io/var-uq]

## The decision hinged on who played the last pass

In soccer, an offside is judged where the attacking team's pass receiver was standing
at the moment the ball was last *played* by a teammate. So in this case the "decision
rule" was

- **No touch:** Perišić's cross is the last played ball. At that moment, Pašalić —
  who went on to set up Gvardiol — was behind the defensive line. Onside. Goal stands.
- **A graze off Matanović:** the graze becomes the new "last played" moment. The clock
  advanced a bit, and in that fraction Pašalić drifted goal-side of the line. That
  counts as offside.

Note that the line itself is a moving target: it sits wherever the second-last
defender happens to be standing, and the defense was collapsing toward goal
throughout the move.

## The sensor has two detection channels

Inside the match ball there's a chip — an IMU, for *inertial measurement unit. *It
combines an accelerometer (which feels jolts and vibrations) and a gyroscope (which
feels rotation), and it reports 500 times per second. Unlike "snicko", there's no
microphone or camera. Snicko listens through the air; while this chip can only feel
its own motion.

[IMAGE 2: sensor/ball diagram]

In the 2022 and 2024 balls, it hung at the center on an elastic suspension — so any
vibration from the surface had to travel down the tethers to be felt. The 2026
Trionda changed this: per Adidas, the chip is now embedded in a special layer
*inside one of the four panels*, with counterweights in the other three to keep the
ball balanced. That's better "coupling" — the shell's vibrations reach the chip
directly — but I think the position of the graze can affect things dramatically: it
can land on the chip's panel or on the far side of the ball, and the latter might
have lower signal to noise ratio.

(I also found out the Trionda shape is a tetrahedron-inspired four-panel design, the
fewest panels in World Cup history. Scientific American has a lovely piece on it.
The Jabulani was a weird "snipped-off" version of the Tetrahedron)

[IMAGE 3 and IMAGE 4, side by side in columns: ball design images]

## What can a chip that only feels motion actually feel?

I enjoyed doing some idealized back-of-the-hand physics to internalize the physics
here. A touch leaves two physical traces for a motion sensor:

1. **Translational, i.e., "the push".**
   1. A graze transfers momentum. How much? Pressing an elevator button is roughly
      1 newton of force; a brush of hair is plausibly somewhere between a hundredth
      and a fifth of that.
   2. And the contact is *brief* — at 20 m/s the ball is past your head in a few
      thousandths of a second, so call it 5 milliseconds of touching.
   3. Multiply force by time and divide by the ball's mass (430 grams, per
      regulation) and the ball's velocity changes by something between **0.1 and 2
      millimeters per second** — on a ball doing 20 meters per second.
   4. Over the half-second of flight that remained, that deflects the ball's path by
      at most a millimeter, and plausibly by roughly 50 microns — *about the width
      of the hair that caused it*. So if there was a deviation, its not noticeable
      at a human-eye-detectable level.

To put a number on the chip's-eye view: during those 5 ms the push produces an
acceleration of a few hundredths to a half of a m/s². The chip's everyday "ride" —
air drag flickering with turbulence and the ball's spin — is tens to hundreds of
times louder. Channel 1 is a whisper in a storm.

1. **A pressure wave, aka "the ring".**
   1. Since a football isn't a rigid billiard ball. It's a pressurized shell — a
      stretched drum skin. Tap a drum and the skin doesn't fly across the room; it
      *shudders*. The graze sets off a vibration in the shell that rings for a few
      hundredths of a second, at hundreds of oscillations per second, long after the
      contact itself has ended. This is, in a satisfying sense, my cricket instinct
      vindicated: sound traveling through a solid *is* a pressure wave. The ball
      hears the touch the way a drum hears a tap — and the accelerometer, riding in
      the shell, feels that ring directly.

**Why the ring wins.** The noise the chip lives with — spin wobble at maybe 8 cycles
per second, turbulent buffeting a bit faster — is all *slow*, by electronics
standards: essentially everything below about 80 Hz. The ring lives up in the
hundreds of Hz. That separation is the whole game. It also explains a design choice
hiding in plain sight: the chip samples 500 times a second, about 25 times faster
than the noise requires. A sampling rate is a confession of what its designers wanted
to see — and 500 Hz says they were provisioning for something *fast*. Once you see
that, the detector nearly designs itself: filter out everything below about 100 Hz
(deafen yourself to the ride), then flag anything that pokes above a threshold in
what remains. I'm fairly sure I "invented" this detector about fifty years after
everyone else, but the point of the exercise was that the logic falls out of the
physics with almost no degrees of freedom.

## What nobody will tell us

Here's the part that surprised me most, and it isn't physics. As far as I can find,
neither FIFA, Adidas, nor KINEXON (the sensor maker) has published *any* of the
quantities that would let an outsider evaluate the system: no detection algorithm,
no threshold, no false-positive or false-negative rate. The public statements are
confidence claims — "rigorously and robustly tested" — and the testing described is
about whether the chip changes how the ball plays, not about how reliably it detects
touches.

There's also a telling precedent I'd completely forgotten until I dug back through
the coverage: Portugal–Uruguay, 2022. Ronaldo claimed a touch on Bruno Fernandes's
goal; FIFA's statement said the sensor data let them "definitively show no contact"
— the *absence* of a heartbeat offered as proof of no touch. Set that beside the
Matanović call, where the *presence* of a heartbeat proved a touch, and you have the
same instrument being read with total confidence in both directions — two different
error types, no error bars either time.

Which brings me to the honest core of the whole investigation. Whether the chip can
hear a hair graze depends overwhelmingly on one number nobody publishes and we
couldn't derive: how strongly the shell's ring couples into the sensor. In our
modeling we called it **κ** (kappa): κ = 0 means none of the ring reaches the chip
(it feels only the hopeless push); higher κ means the ring arrives loud — maybe the
graze landed near the chip's panel, maybe the coupling is just good. Everything
interesting about this system's reliability lives inside that one unknown — and,
thanks to the side-mounted design, κ plausibly *varies from touch to touch depending
on where the ball was grazed*. Same graze, different spot on the ball, different
verdict. I think about that more than I'd like to.

## Where this is going

In the next post I'll take you through the simulation we built: a synthetic 500 Hz
ball-chip, realistic noise, grazes injected at various strengths and durations, and
a detector run over thousands of Monte Carlo trials. One preview, because it
reframed how I think about the whole decision: detection isn't a dial, it's a
**cliff**. Across an impressively narrow band of graze strengths, the detector goes
from *essentially blind* to *essentially perfect* — and my honest Fermi range for "a
graze off hair" straddles that cliff. There's also a blind spot hiding in the contact
duration — the slow, soft brush is the hardest touch in the world to hear, and it is
uncomfortably close to a description of this exact incident.

After that: how other sports do it — cricket's umpire's call as uncertainty written
directly into the laws of a game, and tennis, which measures its line-calling error
to the millimeter and then shows you none of it.

---

## Workshop notes: how this got built

This project is a collaboration with an AI assistant (Claude), and we settled into a
rhythm I can only describe as socratic in both directions. It asked me questions —
one at a time, making me do Fermi estimates before revealing what its simulation
said; I made predictions and got scored. (Round 1: I predicted a push-only detector
catches 1 graze in 100 and a loud-ring detector 99 — the sim said 8 and 100. Round
2: I guessed the detection cliff sits at 0.2 in our graze units; truth was about
0.35. I'm choosing to feel calibrated.) I find myself wanting to dig more, and
*retaining* more — the physics is genuinely delightful, and it took me straight back
to my undergrad EE days. The AI built animations and figures whenever I needed
intuition, we refined an offside schematic through several rounds of my nitpicks
(including checking it against actual broadcast frames), and at one point I caught a
real flaw in one of its figures by asking a single question — the detection threshold
was drawn against the raw signal, when the detector actually operates on a filtered
version the figure never showed. Which, I note with some satisfaction, is precisely
the sin the broadcast heartbeat graphic commits against all of us.

*Next up: "Can a chip in a ball feel a hair?" — the simulation. If you've ever wanted
to watch a World Cup verdict reduced to an ROC curve, this series is for you.* :-)

---

**Sources:** ESPN on the FIFA statement · Goal's coverage · TNT Sports · Adidas
Trionda unveil · FIFA on semi-automated offside · KINEXON · Scientific American on
the Trionda. *Physics numbers are our own order-of-magnitude estimates; no official
detection specs have been published as of July 2026. Working repo, simulation code,
and prediction logs: github.com/shishirdash/var-uq.*
