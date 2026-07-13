"""Can a chip in a ball feel a hair?

Synthetic-IMU study of micro-touch detection for the VAR-UQ blog series.

Model: one accelerometer axis of a sensor suspended at the center of a ball in
flight, sampled internally at 10 kHz, anti-alias filtered and decimated to the
500 Hz the real KINEXON sensor reports. A touch adds (a) a rigid-body half-sine
deceleration pulse with impulse J over contact time tau, and (b) a damped
shell-vibration "shudder" whose amplitude scales with peak contact force via an
unknown coupling kappa_shudder — the honest big unknown, so we sweep it.

Detector: high-pass at 100 Hz (above the aero-noise band), threshold on peak
magnitude. Monte Carlo -> ROC and a detectability map over (J, tau).

# ponytail: single-axis magnitude model, no gyro/UWB fusion; add axes if the
# one-axis conclusion looks threshold-marginal.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

RNG = np.random.default_rng(7)

# --- physical constants -----------------------------------------------------
M_BALL = 0.43        # kg (FIFA law: 410-450 g)
FS_HI = 10_000       # Hz, internal simulation rate
FS = 500             # Hz, sensor reporting rate
DECIM = FS_HI // FS
T_WIN = 0.6          # s, decision window
N_HI = int(T_WIN * FS_HI)

# noise model (m/s^2, single axis)
SIG_AERO = 1.0       # RMS of band-limited aero buffeting (<80 Hz)
F_AERO = 80.0
A_SPIN = 0.7         # spin-wobble amplitude at f_spin
F_SPIN = 8.0
SIG_SENSOR = 0.02    # MEMS noise, ~125 ug/sqrt(Hz) over 250 Hz bandwidth

# shell shudder (the "ring" in early notes)
F_RING = 180.0       # Hz, first shell mode reaching the sensor (below Nyquist)
TAU_RING = 0.03      # s, decay time

FPR_TARGET = 0.01
N_TRIALS = 300

# palette (dataviz reference instance, light mode)
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#898781", "#e1e0d9", "#fcfcfb"
CAT = ["#2a78d6", "#1baf7a", "#eda100", "#008300"]  # fixed slot order
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

_t_hi = np.arange(N_HI) / FS_HI
_f_hi = np.fft.rfftfreq(N_HI, 1 / FS_HI)


def _bandlimit(white, fc):
    """Low-pass white noise (batch, axis=-1) with a soft FFT edge, keep RMS=1."""
    spec = np.fft.rfft(white, axis=-1)
    mask = 1 / (1 + (_f_hi / fc) ** 8)
    out = np.fft.irfft(spec * mask, n=N_HI, axis=-1)
    return out / out.std(axis=-1, keepdims=True)


def make_noise(n):
    """(n, N_HI) noise-only acceleration at 10 kHz."""
    aero = SIG_AERO * _bandlimit(RNG.standard_normal((n, N_HI)), F_AERO)
    phase = RNG.uniform(0, 2 * np.pi, (n, 2, 1))
    spin = A_SPIN * np.sin(2 * np.pi * F_SPIN * _t_hi + phase[:, 0]) \
        + 0.3 * A_SPIN * np.sin(2 * np.pi * 2 * F_SPIN * _t_hi + phase[:, 1])
    sensor = SIG_SENSOR * np.sqrt(FS_HI / FS) * RNG.standard_normal((n, N_HI))
    return aero + spin + sensor


def touch_pulse(J, tau, kappa_shudder):
    """Touch signature at 10 kHz: half-sine rigid pulse + damped shell ring."""
    a = np.zeros(N_HI)
    t0 = T_WIN / 2
    i0 = int(t0 * FS_HI)
    n_c = max(int(tau * FS_HI), 2)
    a_peak = np.pi * J / (2 * M_BALL * tau)
    a[i0:i0 + n_c] += a_peak * np.sin(np.pi * np.arange(n_c) / n_c)
    t_rel = _t_hi[i0 + n_c:] - _t_hi[i0 + n_c]
    a[i0 + n_c:] += kappa_shudder * a_peak * np.exp(-t_rel / TAU_RING) \
        * np.sin(2 * np.pi * F_RING * t_rel)
    return a


def to_sensor(a_hi):
    """Anti-alias to 200 Hz and decimate to 500 Hz — what the chip reports."""
    spec = np.fft.rfft(a_hi, axis=-1)
    spec *= 1 / (1 + (_f_hi / 200.0) ** 8)
    return np.fft.irfft(spec, n=N_HI, axis=-1)[..., ::DECIM]


def highpass(a_500):
    """The detector's ears: kill everything below ~100 Hz (the aero band)."""
    f = np.fft.rfftfreq(a_500.shape[-1], 1 / FS)
    spec = np.fft.rfft(a_500, axis=-1)
    spec *= 1 - 1 / (1 + (f / 100.0) ** 8)
    return np.fft.irfft(spec, n=a_500.shape[-1], axis=-1)


def detect_stat(a_500):
    """Detection statistic: peak |high-pass| above the aero band."""
    return np.abs(highpass(a_500)).max(axis=-1)


def run_cell(J, tau, kappa_shudder, noise_stats):
    """TPR at the FPR_TARGET threshold for one (J, tau, kappa_shudder)."""
    thresh = np.quantile(noise_stats, 1 - FPR_TARGET)
    sig = touch_pulse(J, tau, kappa_shudder)
    stats = detect_stat(to_sensor(make_noise(N_TRIALS) + sig))
    return (stats > thresh).mean()


def styled_axes(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def fig_traces(noise_stats, out):
    cases = [("no touch", 0.0, 0.5),
             ("hair graze, J = 1 mN·s, κ_shudder = 0.5", 1e-3, 0.5),
             ("same hair graze, loud shudder κ_shudder = 2", 1e-3, 2.0),
             ("firm graze, J = 5 mN·s, κ_shudder = 0.5", 5e-3, 0.5)]
    thresh = np.quantile(noise_stats, 1 - FPR_TARGET)
    fig, axes = plt.subplots(4, 1, figsize=(8, 7.6), sharex=True, sharey=True)
    fig.patch.set_facecolor(SURFACE)
    t = np.arange(N_HI // DECIM) / FS * 1000
    for ax, (label, J, kappa_shudder) in zip(axes, cases):
        sig = touch_pulse(J, 5e-3, kappa_shudder) if J else np.zeros(N_HI)
        a = to_sensor(make_noise(1)[0] + sig)
        hp = highpass(a)
        styled_axes(ax)
        ax.plot(t, a, color=INK, lw=0.9, alpha=0.35)
        ax.plot(t, hp, color=CAT[0], lw=1.3)
        ax.axhline(thresh, color=CAT[2], lw=1.2, ls="--")
        ax.axhline(-thresh, color=CAT[2], lw=1.2, ls="--")
        ax.text(0.01, 0.92, label, transform=ax.transAxes, fontsize=10,
                color=INK, va="top")
        if J:
            ax.annotate("contact", (300, hp[int(0.3 * FS)]), fontsize=9,
                        color=MUTED, xytext=(320, 6),
                        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    axes[0].text(0.99, 0.92,
                 "gray: raw signal · blue: after the >100 Hz filter —\n"
                 "the dashes (1% false-alarm threshold) apply to BLUE",
                 transform=axes[0].transAxes, fontsize=9, color=MUTED,
                 va="top", ha="right")
    axes[-1].set_xlabel("time (ms)", color=MUTED)
    fig.supylabel("accelerometer reading (m/s²)", color=MUTED, fontsize=10)
    fig.suptitle("What the 'heartbeat graphic' is drawn from", color=INK,
                 fontsize=12, x=0.02, ha="left")
    fig.tight_layout()
    fig.savefig(out, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def fig_roc(noise_stats, out):
    kappas = [(0.0, "κ_shudder = 0 (push only)"), (0.5, "κ_shudder = 0.5 (faint shudder)"),
              (2.0, "κ_shudder = 2 (loud shudder)")]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.8), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    fpr = np.linspace(0, 1, 200)
    thr = np.quantile(noise_stats, 1 - fpr)
    for ax, (kappa_shudder, title) in zip(axes, kappas):
        styled_axes(ax)
        for J, color in zip([0.5e-3, 1e-3, 2e-3, 5e-3], CAT):
            sig = touch_pulse(J, 5e-3, kappa_shudder)
            stats = detect_stat(to_sensor(make_noise(N_TRIALS) + sig))
            tpr = (stats[:, None] > thr[None, :]).mean(axis=0)
            ax.plot(fpr, tpr, color=color, lw=2, label=f"J = {J*1e3:g} mN·s")
        ax.plot([0, 1], [0, 1], color=GRID, lw=1, ls=":")
        ax.set_xlabel("false-alarm rate", color=MUTED)
        ax.set_title(title, color=INK, fontsize=11, loc="left")
    axes[0].set_ylabel("detection rate", color=MUTED)
    leg = axes[0].legend(loc="lower right", fontsize=9, frameon=False)
    for txt in leg.get_texts():
        txt.set_color(INK)
    fig.suptitle("ROC: graze detection, 5 ms contact — the shudder makes the cliff",
                 color=INK, fontsize=12, x=0.02, ha="left")
    fig.tight_layout()
    fig.savefig(out, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def fig_detectability(noise_stats, out):
    Js = np.geomspace(0.2e-3, 10e-3, 8)
    taus = np.array([1, 2, 5, 10, 20]) * 1e-3
    cmap = LinearSegmentedColormap.from_list("seq", SEQ)
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    for ax, kappa_shudder in zip(axes, [0.0, 0.5, 2.0]):
        grid = np.array([[run_cell(J, tau, kappa_shudder, noise_stats)
                          for J in Js] for tau in taus])
        im = ax.imshow(grid, origin="lower", aspect="auto", cmap=cmap,
                       vmin=0, vmax=1)
        ax.set_xticks(range(len(Js)), [f"{J*1e3:.1f}" for J in Js], fontsize=8)
        ax.set_yticks(range(len(taus)), [f"{tau*1e3:g}" for tau in taus])
        ax.tick_params(colors=MUTED)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_xlabel("impulse J (mN·s)", color=MUTED)
        ax.set_title(f"shudder coupling κ_shudder = {kappa_shudder:g}"
                     + ("  (rigid body only)" if kappa_shudder == 0 else ""),
                     color=INK, fontsize=10, loc="left")
        for (r, c), v in np.ndenumerate(grid):
            ax.text(c, r, f"{v:.2f}", ha="center", va="center", fontsize=7,
                    color=INK if v < 0.6 else SURFACE)
    axes[0].set_ylabel("contact time τ (ms)", color=MUTED)
    fig.colorbar(im, ax=axes, fraction=0.03, pad=0.02,
                 label="detection rate at 1% false-alarm")
    fig.suptitle("Detectability of a graze, 500 Hz ball IMU", color=INK,
                 fontsize=12, x=0.02, ha="left")
    fig.savefig(out, dpi=150, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def main():
    import pathlib

    figs = pathlib.Path(__file__).parent / "figs"
    figs.mkdir(exist_ok=True)

    # fermi context, printed for the blog draft
    drag = 0.5 * 1.2 * 0.25 * (np.pi * 0.11**2) * 20**2
    print(f"drag decel at 20 m/s: {drag / M_BALL:.1f} m/s^2")
    print(f"header impulse ~ {M_BALL * 5:.2f} kg*m/s; "
          f"hair graze ~ 1e-3 kg*m/s -> {M_BALL * 5 / 1e-3:.0f}x smaller")

    noise_stats = detect_stat(to_sensor(make_noise(2000)))

    # self-check: detector sane at the extremes
    assert run_cell(50e-3, 5e-3, 0.5, noise_stats) > 0.99, "big touch missed"
    faint = run_cell(1e-6, 5e-3, 0.5, noise_stats)
    assert abs(faint - FPR_TARGET) < 0.03, f"null TPR {faint} != FPR"

    fig_traces(noise_stats, figs / "fig_traces.png")
    fig_roc(noise_stats, figs / "fig_roc.png")
    fig_detectability(noise_stats, figs / "fig_detectability.png")

    for J in [0.5e-3, 1e-3, 2e-3, 5e-3]:
        for kappa_shudder in [0.0, 0.5, 2.0]:
            tpr = run_cell(J, 5e-3, kappa_shudder, noise_stats)
            print(f"J={J*1e3:4.1f} mN·s  tau=5ms  κ_shudder={kappa_shudder:3.1f}  "
                  f"TPR@1%FPR = {tpr:.2f}")
    print(f"figures -> {figs}")


if __name__ == "__main__":
    main()


# --- gyro channel: the twist (round 3, socratic session 2026-07-07) ---
# Model: single gyro axis at 500 Hz. Baseline spin ~8 rev/s with slow aero
# decay + MEMS white jitter + bias drift (random walk). Graze adds a permanent
# step dw = f * J * r / I. Detector: two-window mean comparison (Shishir's
# design, Q4b), 0.1 s per side, threshold set on noise-only runs at 1% FPR.
# ponytail: scalar spin (no 3-axis precession); add axes if verdicts look marginal.

R_BALL = 0.11
I_BALL = (2 / 3) * M_BALL * R_BALL**2
GYRO_JITTER = 0.15 * np.pi / 180 * 57.3 / 57.3  # keep everything in deg/s
GYRO_JITTER_DPS = 0.15          # white noise per reading, deg/s
DRIFT_RW_DPS = 0.02             # bias random-walk step per sample, deg/s/sqrt(sample)
SPIN0_DPS = 2880.0
AERO_DECAY = 0.01               # fractional spin decay per second
WIN = int(0.1 * FS)             # 50 samples per side
N_G = int(0.6 * FS)             # 0.6 s trace, graze at middle


def gyro_trace(n_trials, J=0.0, kappa_twist=1.0, rng=RNG):
    t = np.arange(N_G) / FS
    base = SPIN0_DPS * (1 - AERO_DECAY * t)
    drift = np.cumsum(rng.standard_normal((n_trials, N_G)) * DRIFT_RW_DPS, axis=1)
    white = rng.standard_normal((n_trials, N_G)) * GYRO_JITTER_DPS
    step = np.zeros(N_G)
    dw_dps = kappa_twist * J * R_BALL / I_BALL * 57.2958
    step[N_G // 2:] = dw_dps
    return base[None, :] + drift + white + step[None, :]


def twist_stat(traces):
    mid = N_G // 2
    before = traces[:, mid - WIN:mid].mean(axis=1)
    after = traces[:, mid:mid + WIN].mean(axis=1)
    return np.abs(after - before)


def gyro_sweep():
    noise = twist_stat(gyro_trace(3000))
    th = np.quantile(noise, 0.99)
    print(f"gyro two-window threshold @1% FPR: {th:.3f} deg/s")
    print(f"{'J (mN.s)':>9} {'κt=1.0':>7} {'κt=0.3':>7}")
    for J in [0.005, 0.01, 0.02, 0.035, 0.05, 0.07, 0.1, 0.2, 0.35, 1.0]:
        row = []
        for kappa_twist in (1.0, 0.3):
            tpr = (twist_stat(gyro_trace(400, J * 1e-3, kappa_twist)) > th).mean()
            row.append(tpr)
        print(f"{J:9.3f} {row[0]:7.2f} {row[1]:7.2f}")


if __name__ == "__main__" and __import__("sys").argv[-1] == "gyro":
    gyro_sweep()


def twist_stat_detrended(traces):
    """Shishir's Q6b fix: fit a line to the before-window, extrapolate it
    under the after-window, subtract, then compare residual means."""
    mid = N_G // 2
    x = np.arange(-WIN, 0) + 0.5          # before-window sample times, centered
    yb = traces[:, mid - WIN:mid]
    xc = x - x.mean()
    slope = (yb * xc).sum(1) / (xc**2).sum()
    intercept = yb.mean(1)
    xa = np.arange(0, WIN) + 0.5 - x.mean()   # after-window, same time origin
    pred = intercept[:, None] + slope[:, None] * xa[None, :]
    resid = traces[:, mid:mid + WIN] - pred
    return np.abs(resid.mean(1))


def gyro_sweep_v2():
    noise = twist_stat_detrended(gyro_trace(3000))
    th = np.quantile(noise, 0.99)
    print(f"detrended threshold @1% FPR: {th:.3f} deg/s")
    print(f"{'J (mN.s)':>9} {'κt=1.0':>7} {'κt=0.3':>7}")
    for J in [0.01, 0.02, 0.035, 0.05, 0.07, 0.1, 0.15, 0.2, 0.35, 0.7, 1.0]:
        row = []
        for kappa_twist in (1.0, 0.3):
            tpr = (twist_stat_detrended(gyro_trace(400, J * 1e-3, kappa_twist)) > th).mean()
            row.append(tpr)
        print(f"{J:9.3f} {row[0]:7.2f} {row[1]:7.2f}")


if __name__ == "__main__" and __import__("sys").argv[-1] == "gyro2":
    gyro_sweep_v2()


def fig_twist_detectability(out):
    Js = np.array([0.01, 0.02, 0.035, 0.05, 0.07, 0.1, 0.15, 0.2, 0.35, 0.7, 1.0])
    th_naive = np.quantile(twist_stat(gyro_trace(3000)), 0.99)
    th_detr = np.quantile(twist_stat_detrended(gyro_trace(3000)), 0.99)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    fig.patch.set_facecolor(SURFACE)
    styled_axes(ax)
    for kappa_twist, color in [(1.0, SEQ[5]), (0.3, SEQ[2])]:
        tpr = [(twist_stat_detrended(gyro_trace(400, J * 1e-3, kappa_twist))
                > th_detr).mean() for J in Js]
        ax.plot(Js, tpr, "o-", color=color, lw=2, ms=5,
                label=f"detrended, κ_twist = {kappa_twist:g}")
    tpr_naive = [(twist_stat(gyro_trace(400, J * 1e-3, 1.0)) > th_naive).mean()
                 for J in Js]
    ax.plot(Js, tpr_naive, "s--", color=MUTED, lw=1.5, ms=4,
            label="naive two-window, κ_twist = 1 (blinded by spin decay)")
    ax.set_xscale("log")
    ax.set_xlabel("impulse J (mN·s)", color=MUTED)
    ax.set_ylabel("detection rate at 1% false-alarm", color=MUTED)
    ax.set_ylim(-0.03, 1.05)
    ax.legend(frameon=False, fontsize=9, labelcolor=INK)
    ax.set_title("Detectability via the twist (gyro), 500 Hz ball IMU",
                 color=INK, fontsize=12, loc="left")
    fig.savefig(out, dpi=150, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__" and __import__("sys").argv[-1] == "gyrofig":
    fig_twist_detectability("figs/fig_twist_detectability.png")
    print("wrote figs/fig_twist_detectability.png")


# --- round 5: audit-corrected inputs (2026-07-08) ---------------------------
# Corrections from research/assumption-audit.md: ride band 80->20 Hz, ride
# amplitude x0.65 (drag 2->1.3 N), gyro white jitter 0.15->0.06 dps.

def _sweep_shudder(Js, kappa=2.0, tau=5e-3, n=400):
    th = np.quantile(detect_stat(to_sensor(make_noise(3000))), 1 - FPR_TARGET)
    return np.array([(detect_stat(to_sensor(make_noise(n) + touch_pulse(J, tau, kappa)))
                      > th).mean() for J in Js])


def _sweep_twist(Js, kappa_twist=1.0, n=400):
    th = np.quantile(twist_stat_detrended(gyro_trace(3000)), 1 - FPR_TARGET)
    return np.array([(twist_stat_detrended(gyro_trace(n, J * 1e-3, kappa_twist))
                      > th).mean() for J in Js])


def _crossing(Js, tpr, level):
    """First J where tpr crosses `level`, log-interpolated. None if never."""
    for i in range(1, len(Js)):
        if tpr[i - 1] < level <= tpr[i]:
            f = (level - tpr[i - 1]) / (tpr[i] - tpr[i - 1])
            return float(np.exp(np.log(Js[i - 1]) + f * np.log(Js[i] / Js[i - 1])))
    return None


def round5():
    global SIG_AERO, F_AERO, GYRO_JITTER_DPS
    Js_s = np.geomspace(0.02, 2.0, 15)   # mN·s, shudder sweep
    Js_t = np.geomspace(0.01, 1.0, 15)   # mN·s, twist sweep

    results = {}
    old = (SIG_AERO, F_AERO, GYRO_JITTER_DPS)
    for tag, (sig, fa, gj) in [("baseline", old), ("corrected", (0.65, 20.0, 0.06))]:
        SIG_AERO, F_AERO, GYRO_JITTER_DPS = sig, fa, gj
        results[tag] = {"shudder": _sweep_shudder(Js_s * 1e-3),
                        "twist": _sweep_twist(Js_t)}
    SIG_AERO, F_AERO, GYRO_JITTER_DPS = old

    for ch, Js in [("shudder", Js_s), ("twist", Js_t)]:
        for tag in ("baseline", "corrected"):
            tpr = results[tag][ch]
            c50 = _crossing(Js, tpr, 0.5)
            c10, c90 = _crossing(Js, tpr, 0.1), _crossing(Js, tpr, 0.9)
            width = (c90 / c10) if (c10 and c90) else float("nan")
            print(f"{ch:8s} {tag:9s}  J50={c50 and f'{c50:.3f}'} mN·s  "
                  f"10->90% width x{width:.2f}")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    for ax, (ch, Js, title) in zip(axes, [
            ("shudder", Js_s, "shudder (κ_shudder = 2, τ = 5 ms)"),
            ("twist", Js_t, "twist (κ_twist = 1, detrended)")]):
        styled_axes(ax)
        ax.plot(Js, results["baseline"][ch], "o--", color=SEQ[2], lw=1.8, ms=4,
                label="post-1 inputs")
        ax.plot(Js, results["corrected"][ch], "o-", color=SEQ[5], lw=2, ms=5,
                label="audit-corrected inputs")
        ax.set_xscale("log")
        ax.set_xlabel("impulse J (mN·s)", color=MUTED)
        ax.set_title(title, color=INK, fontsize=11, loc="left")
        ax.legend(frameon=False, fontsize=9, labelcolor=INK)
    axes[0].set_ylabel("detection rate at 1% false-alarm", color=MUTED)
    fig.suptitle("Round 5: the cliffs under audit-corrected inputs", color=INK,
                 fontsize=12, x=0.02, ha="left")
    fig.savefig("figs/fig_round5_audit.png", dpi=150, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote figs/fig_round5_audit.png")


if __name__ == "__main__" and __import__("sys").argv[-1] == "round5":
    round5()


# --- round 6: psychometric fit (2026-07-11) ----------------------------------
# Logistic in log-J with the detector's 1% FPR floor:
#   p(J) = 0.01 + 0.99 * sigmoid(s * (logJ - logJ50))
# Binomial MLE by vectorized zooming grid search (no scipy in the venv);
# parametric bootstrap for the 95% CI. Inputs = audit-corrected post-2
# baseline (round-5 decision).
# ponytail: grid-search MLE, swap in scipy.optimize if params grow past 2.

CORRECTED = (0.65, 20.0, 0.06)   # SIG_AERO, F_AERO, GYRO_JITTER_DPS


def _psy(logJ, mu, s):
    return FPR_TARGET + (1 - FPR_TARGET) / (1 + np.exp(-s * (logJ - mu)))


def fit_psychometric(Js, k, n, mu0=None, half_mu=1.2, s0=25.0, half_s=24.8):
    """MLE of (logJ50, steepness); zooming grid, 4 rounds of x5 refinement."""
    logJ = np.log(Js)
    mu, s = (np.median(logJ) if mu0 is None else mu0), s0
    for _ in range(4):
        mus = np.linspace(mu - half_mu, mu + half_mu, 41)
        ss = np.linspace(max(s - half_s, 0.2), s + half_s, 41)
        p = np.clip(_psy(logJ, mus[:, None, None], ss[None, :, None]),
                    1e-12, 1 - 1e-12)
        nll = -(k * np.log(p) + (n - k) * np.log1p(-p)).sum(-1)
        i, j = np.unravel_index(nll.argmin(), nll.shape)
        mu, s = mus[i], ss[j]
        half_mu, half_s = half_mu / 5, half_s / 5
    return mu, s


def boot_ci(Js, k, n, n_boot=1000):
    """Parametric bootstrap from the fitted curve -> percentile CIs."""
    mu, s = fit_psychometric(Js, k, n)
    p_hat = _psy(np.log(Js), mu, s)
    draws = np.array([fit_psychometric(Js, kb, n, mu0=mu, half_mu=0.6,
                                       s0=s, half_s=6.0)
                      for kb in RNG.binomial(n, p_hat, (n_boot, len(Js)))])
    return (mu, s), np.percentile(draws[:, 0], [2.5, 97.5]), \
        np.percentile(draws[:, 1], [2.5, 97.5])


def profile_ci(Js, k, n, mu_hat, s_hat):
    """Profile-likelihood 95% CI on logJ50 (chi2, 1 df): independent
    cross-check on the bootstrap — they should agree when the transition
    is well sampled."""
    logJ = np.log(Js)
    mus = mu_hat + np.linspace(-0.15, 0.15, 301)
    ss = np.geomspace(max(s_hat / 5, 0.5), s_hat * 5, 301)
    p = np.clip(_psy(logJ, mus[:, None, None], ss[None, :, None]),
                1e-12, 1 - 1e-12)
    prof = (-(k * np.log(p) + (n - k) * np.log1p(-p)).sum(-1)).min(1)
    ok = mus[prof <= prof.min() + 1.92]
    return np.exp(ok[0]), np.exp(ok[-1])


def round6():
    global SIG_AERO, F_AERO, GYRO_JITTER_DPS
    old = (SIG_AERO, F_AERO, GYRO_JITTER_DPS)
    SIG_AERO, F_AERO, GYRO_JITTER_DPS = CORRECTED

    # self-check: fit recovers a known curve from clean synthetic counts
    Js_chk = np.geomspace(0.05, 1.0, 11)
    mu_c, s_c = fit_psychometric(
        Js_chk, np.round(400 * _psy(np.log(Js_chk), np.log(0.2), 4.0)), 400)
    assert abs(mu_c - np.log(0.2)) < 0.02 and abs(s_c - 4.0) < 0.3, \
        f"fit self-check failed: {mu_c:.3f}, {s_c:.2f}"

    n = 400
    Js_t = np.array([0.01, 0.02, 0.035, 0.05, 0.07, 0.1, 0.15, 0.2, 0.35, 0.7, 1.0])
    th_t = np.quantile(twist_stat_detrended(gyro_trace(3000)), 1 - FPR_TARGET)
    k_t = np.array([(twist_stat_detrended(gyro_trace(n, J * 1e-3, 1.0)) > th_t).sum()
                    for J in Js_t])

    Js_s = np.geomspace(0.02, 2.0, 15)
    th_s = np.quantile(detect_stat(to_sensor(make_noise(3000))), 1 - FPR_TARGET)
    k_s = np.array([(detect_stat(to_sensor(make_noise(n) + touch_pulse(J * 1e-3, 5e-3, 2.0)))
                     > th_s).sum() for J in Js_s])
    SIG_AERO, F_AERO, GYRO_JITTER_DPS = old

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    Jf = np.geomspace(0.008, 2.5, 300)
    for ax, (name, Js, k) in zip(axes, [
            ("twist (κ_twist = 1, detrended)", Js_t, k_t),
            ("shudder (κ_shudder = 2, τ = 5 ms)", Js_s, k_s)]):
        (mu, s), ci_mu, ci_s = boot_ci(Js, k, n)
        J50, lo, hi = np.exp(mu), np.exp(ci_mu[0]), np.exp(ci_mu[1])
        half_pct = (hi - lo) / 2 / J50 * 100
        plo, phi = profile_ci(Js, k, n, mu, s)
        print(f"{name}  counts/{n}: {k.tolist()}")
        w1090 = np.exp(2 * np.log(9) / s)   # 10->90% span of the sigmoid, x-factor in J
        print(f"{name}\n  J50 = {J50:.4f} mN·s\n"
              f"  bootstrap 95% CI [{lo:.4f}, {hi:.4f}] -> ±{half_pct:.1f}%\n"
              f"  profile   95% CI [{plo:.4f}, {phi:.4f}]"
              f" -> ±{(phi - plo) / 2 / J50 * 100:.1f}%\n"
              f"  steepness s = {s:.2f}"
              f" [{ci_s[0]:.2f}, {ci_s[1]:.2f}] -> 10->90% width x{w1090:.2f}")
        styled_axes(ax)
        ax.axvspan(plo, phi, color=SEQ[1], alpha=0.5, lw=0)
        ax.plot(Jf, _psy(np.log(Jf), mu, s), color=SEQ[5], lw=2, label="fitted curve")
        ax.plot(Js, k / n, "o", color=INK, ms=5, label=f"data ({n} trials/point)")
        ax.axvline(J50, color=SEQ[5], lw=1, ls=":")
        ax.set_xscale("log")
        ax.set_xlabel("impulse J (mN·s)", color=MUTED)
        ax.set_title(name, color=INK, fontsize=11, loc="left")
        ax.legend(frameon=False, fontsize=9, labelcolor=INK, loc="upper left")
    axes[0].set_ylabel("detection rate at 1% false-alarm", color=MUTED)
    fig.suptitle("Round 6: psychometric fits, audit-corrected inputs "
                 "(band = 95% CI on J50)", color=INK, fontsize=12, x=0.02, ha="left")
    fig.savefig("figs/fig_round6_fit.png", dpi=150, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote figs/fig_round6_fit.png")


if __name__ == "__main__" and __import__("sys").argv[-1] == "round6":
    round6()


# --- round 7: the staircase (2026-07-13) --------------------------------------
# Shishir's design: blind 15-point grid (6k flights) as the seed, then six
# adaptive waves of 1,000; before each wave, refit on ALL accumulated data,
# draw the surviving curve family (joint 95% likelihood region), and place the
# wave's J values where the family fans widest. Shudder channel, corrected
# inputs. Envelope: final 95% profile CI on J50; side bet: does steepness get
# a finite upper bound.

S_GRID = np.geomspace(5, 500, 201)   # generous: "bounded" must beat the edge


def _nll_grid(Js, k, n, mus, ss):
    p = np.clip(_psy(np.log(Js), mus[:, None, None], ss[None, :, None]),
                1e-12, 1 - 1e-12)
    return -(k * np.log(p) + (n - k) * np.log1p(-p)).sum(-1)


def fan(Js, k, n, mu_hat, Jgrid):
    """Min/max p(J) across the joint-95% surviving family (dnll <= 3.0)."""
    mus = mu_hat + np.linspace(-0.4, 0.4, 201)
    nll = _nll_grid(Js, k, n, mus, S_GRID)
    keep = nll <= nll.min() + 3.0
    p = _psy(np.log(Jgrid), mus[np.where(keep)[0], None],
             S_GRID[np.where(keep)[1], None])
    return p.min(0), p.max(0)


def profile_s(Js, k, n, mu_hat):
    """Profile-likelihood 95% interval on steepness; flags a search-edge hit."""
    mus = mu_hat + np.linspace(-0.4, 0.4, 201)
    prof = _nll_grid(Js, k, n, mus, S_GRID).min(0)
    ok = S_GRID[prof <= prof.min() + 1.92]
    return ok[0], ok[-1], bool(ok[-1] == S_GRID[-1])


def round7():
    global SIG_AERO, F_AERO, GYRO_JITTER_DPS
    old = (SIG_AERO, F_AERO, GYRO_JITTER_DPS)
    SIG_AERO, F_AERO, GYRO_JITTER_DPS = CORRECTED
    th = np.quantile(detect_stat(to_sensor(make_noise(3000))), 1 - FPR_TARGET)

    def run_dot(J, n):
        sig = touch_pulse(J * 1e-3, 5e-3, 2.0)
        return int((detect_stat(to_sensor(make_noise(n) + sig)) > th).sum())

    Js = list(np.geomspace(0.02, 2.0, 15))          # blind seed grid
    ns = [400] * 15
    ks = [run_dot(J, 400) for J in Js]

    Jgrid = np.geomspace(0.05, 1.0, 400)
    fans = {}
    for wave in range(7):                            # wave 0 = seed only
        Jsa, ka, na = map(np.array, (Js, ks, ns))
        mu, s = fit_psychometric(Jsa, ka, na)
        plo, phi = profile_ci(Jsa, ka, na, mu, s)
        J50 = np.exp(mu)
        print(f"wave {wave}: {int(na.sum())} flights, J50 = {J50:.4f}, "
              f"profile CI ±{(phi - plo) / 2 / J50 * 100:.2f}%")
        if wave in (0, 6):
            fans[wave] = fan(Jsa, ka, na, mu, Jgrid)
        if wave == 6:
            break
        pmin, pmax = fan(Jsa, ka, na, mu, Jgrid)
        wide = Jgrid[(pmax - pmin) > 0.5 * (pmax - pmin).max()]
        picks = np.geomspace(wide.min(), wide.max(), 5)
        print(f"  fan widest {wide.min():.3f}-{wide.max():.3f} -> "
              f"placing 5x200 at {[f'{p:.3f}' for p in picks]}")
        for J in picks:
            Js.append(float(J)); ns.append(200); ks.append(run_dot(float(J), 200))

    (mu, s), ci_mu, _ = boot_ci(Jsa, ka, na)
    J50, blo, bhi = np.exp(mu), np.exp(ci_mu[0]), np.exp(ci_mu[1])
    s_lo, s_hi, edge = profile_s(Jsa, ka, na, mu)
    SIG_AERO, F_AERO, GYRO_JITTER_DPS = old
    print(f"\nFINAL (12k flights): J50 = {J50:.4f} mN·s")
    print(f"  profile  95% CI ±{(phi - plo) / 2 / J50 * 100:.2f}%  "
          f"[{plo:.4f}, {phi:.4f}]")
    print(f"  bootstrap 95% CI ±{(bhi - blo) / 2 / J50 * 100:.2f}%  "
          f"[{blo:.4f}, {bhi:.4f}]")
    print(f"  steepness profile [{s_lo:.1f}, {s_hi:.1f}]"
          f"{' — HIT SEARCH EDGE (unbounded)' if edge else ' — bounded'}")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    for w, color, label in [(0, SEQ[2], "after blind grid (6k)"),
                            (6, SEQ[5], "after staircase (12k)")]:
        axes[0].fill_between(Jgrid, *fans[w], color=color, alpha=0.45,
                             lw=0, label=label)
    styled_axes(axes[0])
    axes[0].set_xscale("log")
    axes[0].legend(frameon=False, fontsize=9, labelcolor=INK, loc="upper left")
    axes[0].set_title("the fan: every curve the data can't rule out",
                      color=INK, fontsize=11, loc="left")
    axes[0].set_ylabel("detection rate at 1% false-alarm", color=MUTED)
    styled_axes(axes[1])
    axes[1].axvspan(plo, phi, color=SEQ[1], alpha=0.5, lw=0)
    axes[1].plot(Jgrid, _psy(np.log(Jgrid), mu, s), color=SEQ[5], lw=2,
                 label="final fit")
    sizes = 12 + 30 * (na / 400)
    axes[1].scatter(Jsa, ka / na, s=sizes, color=INK, zorder=3,
                    label="dots (area ~ flights)")
    axes[1].axvline(J50, color=SEQ[5], lw=1, ls=":")
    axes[1].set_xscale("log")
    axes[1].legend(frameon=False, fontsize=9, labelcolor=INK, loc="upper left")
    axes[1].set_title("final fit, 12k flights (band = profile CI)",
                      color=INK, fontsize=11, loc="left")
    for ax in axes:
        ax.set_xlabel("impulse J (mN·s)", color=MUTED)
    fig.suptitle("Round 7: the staircase closes the shudder fan", color=INK,
                 fontsize=12, x=0.02, ha="left")
    fig.savefig("figs/fig_round7_staircase.png", dpi=150, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote figs/fig_round7_staircase.png")


if __name__ == "__main__" and __import__("sys").argv[-1] == "round7":
    round7()
