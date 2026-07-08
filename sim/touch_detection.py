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
