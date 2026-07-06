# Post 1 — "The hair that ended a World Cup run" (working title)

> HOW TO USE THIS FILE: each section has recall prompts. Answer from memory, in
> rough bullets — no looking things up, typos welcome. Mark blanks with `??`.
> Claude edits your answers into prose in your blog voice; facts get checked
> against research/ afterward, not during. The gaps matter as much as the answers.

Style targets: lay-outsider readable · first-person warm · anecdote framing ·
em-dashes fine · curious-reader stance ("to my untrained eyes") · light humor ·
optimistic close · NO policy prescriptions.

---

## 1. Cold open — the moment (your anecdote, not recall)

Where were you watching? What did you feel when Gvardiol slid it in, and then
when the heartbeat graphic appeared? What made YOU suspicious enough to start
this project? (This is the only section that's pure memoir — write it loose.)

- Like most of the world, I found myself gutted by Croatia's VAR-disallowed last-second equalizer against Portugal in their round-of-32 clash. It felt like technology - true to form - had sucked all the joy out of an incredible moment. 
- As someone familiar with cricket's DRS, I was surprised to see the replays show the use of "snicko" to detect the crucial touch from Matanovic. In fact, it turned out to be the *only* indication of a touch, and it ended up being the crucial one. Nothing in the super slow-mos showed any change in ball flight or spin
- That made me think about uncertainty. In a few different ways
  - what precisely was the waveform indicating? (for Fable: maybe we paste a photo of the real waveform?)
  - how wide are the "error bars" ? what do they even mean? 
  - what contributes to noise?
  - how is the sensor set up? i had heard of a chip inside the ball, how does does that work to increase SNR?
  - how does this work with other sensors? like for instance, is there uncertainty in the offside line detection itself that compounds the noise in the overall system?
  - what about physical uncertainties? air turbulence, spin, magnitudie of the bump, velocity and angle of the ball, velcity and angle of the jumping player?
  - how do other sports do it? cricket's DRS system is pretty uncontroversial, and they have a clear set of rules for "umpire's call". is that possible or necessary for this sort of situation?
  - ... etc

## 2. The rule, replayed both ways

From memory: why did an invisible touch flip Pašalić from onside to offside?
What are the two "evaluation moments," and what does the rule compare at each?

- perisic makes the initial cross, it passes close to a bunch of different heads including matanovic's
- palasic heads it facing slightly diagnoal i think
- gvardiol hits it while onrushing towards goal
- replays showed matanovic rising to try to meet the ball and _maybe_ just grazing it
- the offside rests on whether that graze happened. without that graze, palasic is onside wrt perisic's cross. 
- matanovic's touch - if true -  changes the offside line slightly and makes the assessment happen wrt to _his_ touch (not perisic's) since its the last one. 


## 3. The machine that made the call

From memory: what's actually inside the ball? (What does it measure, how often,
what does it NOT have, and where does it sit in the 2026 ball — and why did that
last fact change our thinking?)

- an Inertial Measurement Unit (IMU) that is a combined accelerometer and gyroscope 
- the IMU samples data at 500 Hz. it is set to pick up both force changes and angular changes (?? unsure abt this)
- Trionda balls - unlike the pre-2026 balls which have it at the center - have the IMU on the side panel. when its at the center, the pressure wave from a bump first has to travel through some wire / scaffolding (?? material?). when its on the side panel, there's a more direct measurement, but of course the point of the bump on the ball panel changes the error calculus (if its far away from the sensor point, presumably the wave has to travel farther and ths can be further dampened by other noise)

## 4. What can a chip that only feels motion actually feel?

The heart of the post — your Fermi chain. From memory:
- How big is a hair-graze impulse, roughly, and what everyday comparison did we
  land on for the ball's deflection?
- The two physical channels the graze creates — name them, describe each in one
  sentence, and say which one the chip can realistically hear.
- Where does the noise live (and why), and what does the 500 Hz sampling rate
  "confess" about what the designers wanted to see?
- The detector you re-invented: what's the two-step trick?

- there are two possible channels for the sensor detection: 
  - translational motion from the bump
  - the ball surface "thrum" from the pressure wave. sort of like a stretched drum surface
- translational:
  - an elevator button push is roughly 1N of force
    - so a hair graze / slight touch maybe is between 0.01 to 0.2 N?
    - the touch lasts maybe about 0.5s
    - so impulse (momentum) into the ball surface = force times time = between 0.005 to 0.1 kg-m/s
  - a ball is between 420 - 450g per FIFA regulations. lets assume 430 g
    - momentum must be preserved: so the change in ball speed due to the incoming bump is (momentum divided by mass) = 0.005 / 0.43 to 0.1 / 0.43 = 0.011 to 0.23 m per s
    - angle of impact would change this a fair bit. but we're being conservative here by assuming a 90 deg impact (??), since that would lead to the maximum transfer of momentum
  - ball's traveling at say 20 m/s (?? there must be some uncertainty here too?)
  - so compared to the ball's motion, the change in speed is pretty small. 
  - (for fable: im not quite sure how the accelerometer works to detect the speed change)
- pressure wave or "ring": detected by gyro, similar to the cricket snicko in that the pressure wave is analogous to the sound wave
  - (?? i forget the full formula, but i remember something about squared relationship: iirc, air resistance is higher for a bigger sphere since the surface area is 4*pi*r^2, where r is the sphere radius)
  - this is a bigger signal and is more detectable in some ways
  - one big confounder is air turbulence and this is manifested by the gyro as a sort of continuous flicker, basically at the ball's spin velocty. (i forget the exact numbers) but the frequency of this turns out to be a tenth of the sensor's sampling rate, comfortably outside of the nyquist / aliasing frequency (we may want to explain this in the post)
  - there are other slower-frequency noisy flickers that the sensor also picks up. but since the bump is a short lived pulse, it registers on the power spectrum as a high frequency peak 
  - so we can remove a bunch of the noise with a high pass filter (for fable: are there possible legitimate soccer actions that could act in the low frequency range and thus be missed?)
- the net result is that of the two channels, the pressure wave (or more specifically the power spectral peak from the bump's pulse) is much more detectable than the translational motion from the bump

## 5. What nobody will tell us

From memory: what has FIFA/Adidas/KINEXON published about how touch detection
works — thresholds, error rates, algorithm? What did the 2022 Ronaldo precedent
claim, and what's asymmetric about that case vs. Matanović's? What's κ and why
is it THE unknown?

- nothing that im aware of on sensor thresholds, error rates, algo. there is research from sciam on the shape of the ball (tetrahedral; which might be a fun aside for the post? or if it affects teh UQ piece maybe we can do some digging or preview a future post) 
- i dont remember the 2022 ronaldo precedent (did we discuss this?)
- we can model / simulate scenarios where the "ring / pressure wave" is directly coupled to the trionda imu sensor as opposed to farther away from it or poorly coupled. lets call this coupling factor kappa. this is a key unknown for us since we don't know specifics of the sensor algo
- we'll use a higher kappa to indicate a clear ("loud") wave detection. e.g., maybe the bump is very close to the sensor or there is less ambient turbulence to fight against

## 6. Teaser for post 2 (one paragraph)

From memory: what did the simulation show about detection being a "cliff"? Where
did your predictions land in rounds 1 and 2? (Don't polish — just the beats.)

- (im actually stil a bit unsure i understand this but let me try)
- at each combo of kappa, bump force, and time duration of bump, we can calculate how much of the pressure wave "survives" the HPF (?? i think there is an additional threshold too). 
  - we can build an ROC curve from this thresholding for this specific combo
- we can then vary kappa, bump force and time duration across a grid and try to find which combos get us the most sensitivity at a maximum FPR (say 1%)
- when we do the sim, we see that there's a sort of "cliff" - the sensitivity of detection rapidly falls off for certain combos. 
  - e.g., for the same force (say a graze) and a half-second duration, we see the cliff happen at kappa around 0.35, assuming everything else is constant. 
  - (?? unsure what this implies because 0.35 kappa is hard to build intuition around)

## 7. Workshop notes — how I built this with an AI (sidebar)

Your reflections, not recall: what was it like working socratically — the
predictions, the animation ping-pong, catching the figure flaw by asking one
question? What surprised you about the process?

- fun!
- i find myself wanting to dig more, and retaining more. 
- the physics are genuinely fascinating and reminded me of my phd and undergrad days in ee / ml etc
- fable did a nice job creating animations and visuals when i needed them to build intuition. 
- some of the offside graphic was a bit off which we refined through iterations. 

## 8. Close

Optimistic forward-look + promise of the series. (One or two lines, your voice.)

- im sure you can come up with sometghing here
