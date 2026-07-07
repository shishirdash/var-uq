(Snapshot of the private Notion draft, 2026-07-07, v2 — post hand-refinements.)

# On offsides and uncertainty

I was gutted by Croatia's disallowed last-gasp equalizer against Portugal in their
World Cup 2026 round-of-32 clash. With possibly the last kick of the game, Gvardiol
had buried an equalizer, but was adjudged offside by VAR. It felt like technology —
true to form — had sucked all the joy out of an incredible moment.

As someone who grew up on cricket's Decision Review System (DRS), I was surprised to
see the replays lean on "snicko". A heartbeat-style waveform was shown on TV as proof
that the ball had grazed Matanović's head on its way through the box. Nothing in the
super slow-mos showed any change in the ball's flight or spin, so I assume "snicko"
was the deciding factor.

[IMAGE: broadcast screenshot — the heartbeat waveform graphic shown on TV]

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
- ….

With Claude, I've been trying a sort of Q&A approach to learning new things¹. I
thought this could be a good topic for a similar approach. With Fable this has been
especially fun, since I can generally "one-shot" create some animations, or setup
holistic simulations to test my understanding.

[EMBED: Schematics of the play, the sensor inside the ball, the two detection
channels, and the full flight (four tabs, interactive). Also at
shishirdash.github.io/var-uq]

## The decision hinges on who played the last pass

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

## The chip inside the ball

Inside the match ball there's an IMU, for *inertial measurement unit. *It combines an
accelerometer (which feels jolts and vibrations) and a gyroscope (which feels
rotation), and it reports 500 times per second. Unlike "snicko", there's no
microphone or camera. Snicko listens through the air; while this chip can only feel
its own motion.

[IMAGE: sensor/ball diagram]

In the 2022 and 2024 balls, it hung at the center on an elastic suspension — so any
vibration from the surface had to travel down the tethers to be felt. The 2026
Trionda² changed this: per Adidas, the chip is now embedded in a special layer
*inside one of the four panels*, with counterweights in the other three to keep the
ball balanced. That's better "coupling" — the shell's vibrations reach the chip
directly — but I think the position of the graze can affect things dramatically: it
can land on the chip's panel or on the far side of the ball, and the latter might
have lower signal to noise ratio.

A touch leaves at least two physical traces for a motion sensor, the "push" and the
"shudder", and the shudder is higher signal-to-noise ratio (SNR).

[EMBED: The two channels, animated: the push vs. the shudder (interactive)]

**Translational, i.e., "the push".**

1. A graze transfers momentum from the player to the ball = Mass * Velocity = Force *
   time_duration
2. Pressing an elevator button is roughly 1 newton of force; we can assume a brush of
   hair is between a hundredth and a fifth of that.
3. At 20 m/s the ball is past a head in ~5 milliseconds of touching.
4. Multiply force by time and divide by the ball's mass (430 grams, per regulation)
   and the ball's velocity changes by something between **0.1 and 2 millimeters per
   second** — on a ball doing 20 meters per second.
5. Over the half-second of flight that remained, that deflects the ball's path by at
   most a millimeter, and plausibly by roughly 50 microns = ~width of the hair that
   caused it.
6. The chip's everyday "ride" — air drag flickering with turbulence and the ball's
   spin — is tens to hundreds of times louder.

** pressure wave, i.e.,  "the shudder".**

1. A soccer ball also has properties of "pressurized shell" or  "stretched drum
   skin".
2. The graze sets off a shudder for a few hundredths of a second, at hundreds of
   oscillations per second. This is similar to cricket's "snicko". The accelerometer,
   riding in the shell, feels this too.
3. Compared to the background noise of spin-wobble, which is ~8Hz, this shudder is
   more detectable. I think because it is more like a short fast pulse, it lives in
   the high frequency part of the spectrum
4. The chip samples 500 times a second, about 25 times faster than the noise
   requires. Also comfortably higher than the "Nyquist" frequency, which prevents
   aliasing.
5. So a decent denoising design would be to filter out everything below about 100 Hz
   (deafen yourself to the ride), then flag anything that pokes above a threshold in
   what remains.

## Simulating uncertainty

I couldn't find published work by FIFA, Adidas, or KINEXON (the sensor maker) on the
detection algorithm, threshold, or evaluations. Simulations can help us understand
these better. (Here's my code if you'd like to jump ahead)

A fun "full flight" animation to show the situation: the ride the chip lives with
(spin, drag, turbulence), the graze in slow motion, and the chip recording. The path
deviation is exaggerated ×10,000 by default; press ×1 to see reality, where nothing
visible happens to the ball and the entire verdict lives in the blue line.

[EMBED: full-flight animation]

Whether the chip can hear a hair graze depends how strongly the shell's shudder
couples into the sensor. In my sim, I'm calling it **κ** (kappa): κ = 0 means none of
the shudder reaches the chip (it feels only the small push); higher κ means the
shudder arrives loud — maybe the graze landed near the chip's panel, maybe the
coupling is just good.

Thanks to the side-mounted design, κ plausibly varies depending on where the ball was
grazed.

## Where this is going

In the next post I'll take you through the simulation we built: a synthetic 500 Hz
ball-chip, realistic noise, grazes injected at various strengths and durations, and a
detector run over thousands of Monte Carlo trials. One preview, because it reframed
how I think about the whole decision: detection isn't a dial, it's a **cliff**.
Across an impressively narrow band of graze strengths, the detector goes from
*essentially blind* to *essentially perfect* — and my honest Fermi range for "a graze
off hair" straddles that cliff. There's also a blind spot hiding in the contact
duration — the slow, soft brush is the hardest touch in the world to hear, and it is
uncomfortably close to a description of this exact incident.

After that: how other sports do it — cricket's umpire's call as uncertainty written
directly into the laws of a game, and tennis, which measures its line-calling error
to the millimeter and then shows you none of it.

---

*Next up: "Can a chip in a ball feel a hair?" — the simulation. If you've ever wanted
to watch a World Cup verdict reduced to an ROC curve, this series is for you.* :-)

---

> *Physics numbers are our own order-of-magnitude estimates; no official detection
> specs have been published as of July 2026. Working repo, simulation code, and
> prediction logs: github.com/shishirdash/var-uq.*
>
> 1. Process with Claude: read and dig interactively, get quizzed, and sometimes
>    code, then reveal. E.g., the back-of-the-envelope physics, or guesstimating sim
>    results step by step. I find myself wanting to dig more and retaining the physics
>    better. With Fable, I can generally "one-shot" create some animations, or setup
>    holistic simulations to test my understanding. Not perfect though, e.g., the
>    offside schematic needed several rounds of my nitpicks (including checking it
>    against actual broadcast frames). I also caught a flaw in one of its figures
>    asking why the detection threshold was drawn against the raw signal, when the
>    detector actually operates on a filtered version.
> 2. I also found out the Trionda shape is a tetrahedron-inspired four-panel design,
>    the fewest panels ever. Scientific American has a lovely piece on it. The
>    Jabulani was a weird "snipped-off" version of the Tetrahedron which made it the
>    roundest ball ever, but also the most hated since it was very unpredictable in
>    flight!
> 3. **Sources:** ESPN on the FIFA statement · Goal's coverage · TNT Sports · Adidas
>    Trionda unveil · FIFA on semi-automated offside · KINEXON · Scientific American
>    on the Trionda
