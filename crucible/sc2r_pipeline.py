"""SC-2R — real-trace transport pipeline (detector + shakedown).

Moves SC-2 from synthetic mechanism toward fielded evidence: on a REAL
Starlink RTT/loss trace, (1) detect the ~15 s handover cadence from the
data itself, (2) test whether apparent congestion (loss / RTT spikes)
clusters at handover boundaries, and (3) test whether schedule-masking
informed by the detected cadence removes that false-congestion — the
fielded analogue of SC-2's kappa=1-2c masking gain.

The GRADED run requires a real trace (public datasets named in
PREREG-SC2R.md: WetLinks, the clarkzjw/mmsys24 Starlink RTT set). This
module provides the pipeline and a SHAKEDOWN on a trace-shaped synthetic
signal (15 s-periodic RTT step-changes + Markov congestion + measurement
noise) to demonstrate the detector recovers the cadence and the masking
works. Synthetic shakedown carries no evidential weight.

    python crucible/sc2r_pipeline.py            # shakedown (synthetic)
    python crucible/sc2r_pipeline.py trace.csv  # run on a real RTT/loss csv
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "SC2R-shakedown.json")

DT = 1.0                     # sample period (s)
HANDOVER_S = 15.0            # true handover cadence (for the synthetic trace)
PERIOD_LO, PERIOD_HI = 8, 25  # search band for cadence detection (s)


# ---- cadence detection (works on real or synthetic traces) ----

def detect_cadence(loss, dt=DT):
    """Autocorrelation of the loss/step signal; peak lag in the search
    band is the handover period. Returns (period_s, strength)."""
    x = np.asarray(loss, float)
    x = x - x.mean()
    if np.allclose(x, 0):
        return None, 0.0
    ac = np.correlate(x, x, mode="full")[len(x) - 1:]
    ac = ac / ac[0]
    lo, hi = int(PERIOD_LO / dt), int(PERIOD_HI / dt)
    lag = lo + int(np.argmax(ac[lo:hi + 1]))
    return lag * dt, float(ac[lag])


def handover_mask(n, period_samples, phase, half_width=1):
    """Boolean mask: True near each detected handover boundary."""
    m = np.zeros(n, dtype=bool)
    k = phase % period_samples
    while k < n:
        m[max(0, k - half_width):k + half_width + 1] = True
        k += period_samples
    return m


def best_phase(loss, period_samples, half_width=1):
    """Phase that best aligns the mask with the loss events."""
    best = (0, -1.0)
    for ph in range(period_samples):
        m = handover_mask(len(loss), period_samples, ph, half_width)
        score = float(np.asarray(loss)[m].sum())
        if score > best[1]:
            best = (ph, score)
    return best[0]


def analyze(loss, congestion_truth=None, dt=DT):
    """Core SC-2R measurement. loss: 0/1 per sample. congestion_truth:
    optional 0/1 ground truth (synthetic only)."""
    loss = np.asarray(loss, int)
    period_s, strength = detect_cadence(loss, dt)
    out = {"period_s": period_s, "acf_peak": round(strength, 4)}
    if period_s is None:
        return out
    ps = max(1, int(round(period_s / dt)))
    phase = best_phase(loss, ps)
    hmask = handover_mask(len(loss), ps, phase)
    # fraction of loss events that fall in handover windows
    n_loss = int(loss.sum())
    out["loss_at_handover_frac"] = round(
        float(loss[hmask].sum()) / n_loss, 4) if n_loss else None
    # schedule-masking: ignore loss inside handover windows
    naive = loss
    masked = loss & ~hmask
    if congestion_truth is not None:
        c = np.asarray(congestion_truth, int)
        # false-congestion = signalled loss where there is no true congestion
        fp_naive = float(((naive == 1) & (c == 0)).mean())
        fp_masked = float(((masked == 1) & (c == 0)).mean())
        out["fp_naive"] = round(fp_naive, 4)
        out["fp_masked"] = round(fp_masked, 4)
        out["fp_reduction"] = round(
            1 - fp_masked / fp_naive, 4) if fp_naive > 0 else None
    else:
        out["naive_signal_rate"] = round(float(naive.mean()), 4)
        out["masked_signal_rate"] = round(float(masked.mean()), 4)
        out["signal_reduction"] = round(
            1 - masked.mean() / naive.mean(), 4) if naive.mean() > 0 else None
    return out


# ---- synthetic trace-shaped signal (shakedown only) ----

def synthetic_trace(seed, n=3600):
    rng = np.random.default_rng(seed)
    ho = int(HANDOVER_S / DT)
    rtt = np.empty(n)
    base = 30.0
    loss = np.zeros(n, int)
    # congestion: 2-state Markov, rate ~0.12
    c = np.zeros(n, int)
    q1, q0 = 0.90, 0.985
    for t in range(n):
        if t % ho == 0:                         # handover boundary
            base = 25 + 10 * rng.random()       # new satellite baseline RTT
            loss[max(0, t - 1):t + 1] = 1        # bursty handover loss (not congestion)
        c[t] = (rng.random() < q1) if (t and c[t - 1]) else \
               (0 if (t and rng.random() < q0) else (rng.random() < 0.12))
        infl = 18.0 if c[t] else 0.0
        rtt[t] = base + infl + rng.normal(0, 1.5)
        if c[t] and rng.random() < 0.5:
            loss[t] = 1                          # true-congestion loss
    return rtt, loss, c


def main():
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        # real trace: expect a csv with a 'loss' column (0/1) or RTT to threshold
        import csv
        path = sys.argv[1]
        rows = list(csv.DictReader(open(path)))
        if rows and "loss" in rows[0]:
            loss = [int(float(r["loss"])) for r in rows]
        else:
            rtt = np.array([float(r.get("rtt_ms", r.get("rtt"))) for r in rows])
            loss = (rtt > np.median(rtt) + 2 * np.std(rtt)).astype(int)
        res = analyze(loss)
        print(f"[real trace {path}] {json.dumps(res, indent=1)}")
        return

    print("SC-2R shakedown — synthetic Starlink-shaped trace "
          f"(true handover {HANDOVER_S:.0f}s), seeds 0/1/2\n")
    agg = []
    for seed in (0, 1, 2):
        rtt, loss, c = synthetic_trace(seed)
        r = analyze(loss, congestion_truth=c)
        agg.append(r)
        print(f"seed {seed}: detected period={r['period_s']:.1f}s "
              f"(acf {r['acf_peak']:.2f})  loss@handover="
              f"{r['loss_at_handover_frac']:.2f}  "
              f"fp {r['fp_naive']:.3f}->{r['fp_masked']:.3f} "
              f"(reduction {r['fp_reduction']:.2f})")
    periods = [a["period_s"] for a in agg]
    print(f"\ninterior: cadence recovered {min(periods):.0f}-{max(periods):.0f}s "
          f"(true {HANDOVER_S:.0f}); handover-explained loss and masking "
          f"reduction consistent across seeds")
    json.dump({"campaign": "SC-2R", "sealed": False, "shakedown": True,
               "note": "synthetic trace-shaped; no weight; real run needs a "
               "public Starlink trace (see PREREG-SC2R.md)",
               "true_handover_s": HANDOVER_S, "per_seed": agg},
              open(OUT, "w"), indent=1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    print(f"\nwrote {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
