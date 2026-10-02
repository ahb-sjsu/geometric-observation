"""POST HOC (written 2026-10-02 after registration 4 was scored; descriptive, not a test).
The near-boundary criterion compares the measured removal with ZERO, but its cases have predicted removals anywhere in
[0, 0.05) bit. This compares the 20-split replicate mean with the PREDICTION instead of with zero."""
import json, math
import numpy as np
R = 20
SYN = {"Gauss8", "GaussCoupled", "GaussCoupled-s11", "Gauss8-s12"}
rows = json.load(open("s2noise_measured.json"))
for grp, rs in (("REAL", [r for r in rows if r["dataset"] not in SYN]), ("CONTROL", [r for r in rows if r["dataset"] in SYN])):
    pred = np.array([r["pred_removed"] for r in rs]); mean = np.array([r["mean_rep"] for r in rs])
    sd = np.array([r["sd_rep"] for r in rs]); se_mean = sd / math.sqrt(R)
    print(f"== {grp} n={len(rs)}: predicted removal median {np.median(pred):.4f} (range {pred.min():.4f}..{pred.max():.4f})")
    print(f"   |replicate mean - 0|    median {np.median(np.abs(mean)):.4f};  > 3 SE_mean in {np.mean(np.abs(mean) > 3 * se_mean):.1%}")
    print(f"   |replicate mean - pred| median {np.median(np.abs(mean - pred)):.4f};  > 3 SE_mean in {np.mean(np.abs(mean - pred) > 3 * se_mean):.1%}")
    print(f"   original measured within 2 SE of the PREDICTION: {np.mean([abs(r['measured_removed'] - r['pred_removed']) <= 2 * r['se'] for r in rs]):.1%}"
          f"  (of zero: {np.mean([abs(r['measured_removed']) <= 2 * r['se'] for r in rs]):.1%})")
    print(f"   signed (replicate mean - pred): median {np.median(mean - pred):+.4f}, positive in {np.mean(mean - pred > 0):.1%}")
