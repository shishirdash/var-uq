"""Can a chip in a ball feel a hair?

Synthetic-IMU study of micro-touch detection for the VAR-UQ blog series.

Model: one accelerometer axis of a sensor suspended at the center of a ball in
flight, sampled internally at 10 kHz, anti-alias filtered and decimated to the
500 Hz the real KINEXON sensor reports. A touch adds (a) a rigid-body half-sine
deceleration pulse with impulse J over contact time tau, and (b) a damped
shell-vibration "ring" whose amplitude scales with peak contact force via an
unknown coupling kappa — the honest big unknown, so we sweep it.

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

# shell ring
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


def touch_pulse(J, tau, kappa):
    """Touch signature at 10 kHz: half-sine rigid pulse + damped shell ring."""
    a = np.zeros(N_HI)
    t0 = T_WIN / 2
    i0 = int(t0 * FS_HI)
    n_c = max(int(tau * FS_HI), 2)
    a_peak = np.pi * J / (2 * M_BALL * tau)
    a[i0:i0 + n_c] += a_peak * np.sin(np.pi * np.arange(n_c) / n_c)
    t_rel = _t_hi[i0 + n_c:] - _t_hi[i0 + n_c]
    a[i0 + n_c:] += kappa * a_peak * np.exp(-t_rel / TAU_RING) \
        * np.sin(2 * np.pi * F_RING * t_rel)
    return a


def to_sensor(a_hi):
    """Anti-alias to 200 Hz and decimate to 500 Hz — what the chip reports."""
    spec = np.fft.rfft(a_hi, axis=-1)
    spec *= 1 / (1 + (_f_hi / 200.0) ** 8)
    return np.fft.irfft(spec, n=N_HI, axis=-1)[..., ::DECIM]


def detect_stat(a_500):
    """Detection statistic: peak |high-pass| above the aero band."""
    f = np.fft.rfftfreq(a_500.shape[-1], 1 / FS)
    spec = np.fft.rfft(a_500, axis=-1)
    spec *= 1 - 1 / (1 + (f / 100.0) ** 8)
    return np.abs(np.fft.irfft(spec, n=a_500.shape[-1], axis=-1)).max(axis=-1)


def run_cell(J, tau, kappa, noise_stats):
    """TPR at the FPR_TARGET threshold for one (J, tau, kappa)."""
    thresh = np.quantile(noise_stats, 1 - FPR_TARGET)
    sig = touch_pulse(J, tau, kappa)
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
             ("hair graze, J = 1 mN·s, ring κ = 0.5", 1e-3, 0.5),
             ("same hair graze, loud ring κ = 2", 1e-3, 2.0),
             ("firm graze, J = 5 mN·s, ring κ = 0.5", 5e-3, 0.5)]
    thresh = np.quantile(noise_stats, 1 - FPR_TARGET)
    fig, axes = plt.subplots(4, 1, figsize=(8, 7.6), sharex=True, sharey=True)
    fig.patch.set_facecolor(SURFACE)
    t = np.arange(N_HI // DECIM) / FS * 1000
    for ax, (label, J, kappa) in zip(axes, cases):
        sig = touch_pulse(J, 5e-3, kappa) if J else np.zeros(N_HI)
        a = to_sensor(make_noise(1)[0] + sig)
        styled_axes(ax)
        ax.plot(t, a, color=INK, lw=1.0)
        ax.axhline(thresh, color=CAT[2], lw=1.2, ls="--")
        ax.axhline(-thresh, color=CAT[2], lw=1.2, ls="--")
        ax.text(0.01, 0.92, label, transform=ax.transAxes, fontsize=10,
                color=INK, va="top")
        if J:
            ax.annotate("contact", (300, a[int(0.3 * FS)]), fontsize=9,
                        color=MUTED, xytext=(320, 6),
                        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    axes[0].text(0.99, 0.92, "dashes: detector threshold (1% false-alarm)",
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
    kappas = [(0.0, "κ = 0 (push only)"), (0.5, "κ = 0.5 (faint ring)"),
              (2.0, "κ = 2 (loud ring)")]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.8), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    fpr = np.linspace(0, 1, 200)
    thr = np.quantile(noise_stats, 1 - fpr)
    for ax, (kappa, title) in zip(axes, kappas):
        styled_axes(ax)
        for J, color in zip([0.5e-3, 1e-3, 2e-3, 5e-3], CAT):
            sig = touch_pulse(J, 5e-3, kappa)
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
    fig.suptitle("ROC: graze detection, 5 ms contact — the ring makes the cliff",
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
    for ax, kappa in zip(axes, [0.0, 0.5, 2.0]):
        grid = np.array([[run_cell(J, tau, kappa, noise_stats)
                          for J in Js] for tau in taus])
        im = ax.imshow(grid, origin="lower", aspect="auto", cmap=cmap,
                       vmin=0, vmax=1)
        ax.set_xticks(range(len(Js)), [f"{J*1e3:.1f}" for J in Js], fontsize=8)
        ax.set_yticks(range(len(taus)), [f"{tau*1e3:g}" for tau in taus])
        ax.tick_params(colors=MUTED)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.set_xlabel("impulse J (mN·s)", color=MUTED)
        ax.set_title(f"ring coupling κ = {kappa:g}"
                     + ("  (rigid body only)" if kappa == 0 else ""),
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
        for kappa in [0.0, 0.5, 2.0]:
            tpr = run_cell(J, 5e-3, kappa, noise_stats)
            print(f"J={J*1e3:4.1f} mN·s  tau=5ms  kappa={kappa:3.1f}  "
                  f"TPR@1%FPR = {tpr:.2f}")
    print(f"figures -> {figs}")


if __name__ == "__main__":
    main()
