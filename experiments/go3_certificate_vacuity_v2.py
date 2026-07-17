# Geometric Observation — GO-3 v2: certificate vacuity predicts retrieval death.
# Governed by prereg/GO-P-2026-013 (sealed 4e0b2a88; registered commit 2ed4a9f).
# Corrects GO-P-2026-012's degenerate run: query noise z ~ N(0, I_D/D) (was
# N(0,I_D)) so the sigma-sweep spans alive->dead. Certificate + DERIVED threshold
# mu_crit = E[max of (N-1) standard normals] unchanged. MIT License.
"""GO-3 v2: does the certificate's vacuity threshold locate where retrieval dies?"""

from __future__ import annotations

import json

import numpy as np

D_DEF, N_DEF, QN = 64, 2000, 400


def _unit(x):
    return x / (np.linalg.norm(x, axis=1, keepdims=True) + 1e-12)


def _items(family, N, D, seed):
    r = np.random.default_rng(seed)
    if family == "iso":
        e = r.standard_normal((N, D))
    elif family == "aniso":
        spec = np.geomspace(1.0, 0.05, D).astype(np.float32)
        e = r.standard_normal((N, D)) * np.sqrt(spec)[None, :]
    elif family == "heavytail":
        e = r.standard_t(3, (N, D))
    else:
        raise ValueError(family)
    return _unit(e.astype(np.float32))


def _mu_crit(N, seed=12345, T=4000):
    """Derived constant: E[max of (N-1) standard normals], Monte-Carlo."""
    rng = np.random.default_rng(seed)
    m = N - 1
    # chunk to bound memory
    vals = []
    done = 0
    while done < T:
        b = min(500, T - done)
        vals.append(rng.standard_normal((b, m)).max(1))
        done += b
    return float(np.concatenate(vals).mean())


def _corpus(family, N, D, sigma, seed):
    e = _items(family, N, D, seed)
    r = np.random.default_rng(seed + 1)
    t = r.integers(0, N, QN)
    z = (r.standard_normal((QN, D)) / np.sqrt(D)).astype(np.float32)   # ||z|| ~ 1, matches unit items
    q = _unit(e[t] + sigma * z)
    S = q @ e.T                                  # (QN, N)
    true = S[np.arange(QN), t]
    recall = float((S.argmax(1) == t).mean())
    top10 = float(np.mean([t[j] in np.argpartition(-S[j], 10)[:10] for j in range(QN)]))
    tot, totsq = S.sum(), (S * S).sum()
    cnt = QN * (N - 1)
    m_d = (tot - true.sum()) / cnt
    var_d = (totsq - (true * true).sum()) / cnt - m_d * m_d
    s_d = float(np.sqrt(max(var_d, 1e-12)))
    m_t = float(true.mean())
    mu_hat = (m_t - m_d) / s_d
    mu_c = _mu_crit(N)
    return {"family": family, "N": N, "D": D, "sigma": sigma,
            "recall": recall, "top10": top10, "mu_hat": float(mu_hat),
            "mu_crit": mu_c, "rho": float(mu_hat / mu_c), "m_t_raw": m_t}


def _spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    return float((rx * ry).sum() / (np.sqrt((rx * rx).sum() * (ry * ry).sum()) + 1e-12))


def main():
    grid = []
    for s in [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]:
        grid.append(("iso", N_DEF, D_DEF, s, 100 + int(s * 10)))
    for s in [1.5, 2.5]:
        grid.append(("aniso", N_DEF, D_DEF, s, 300 + int(s * 10)))
        grid.append(("heavytail", N_DEF, D_DEF, s, 400 + int(s * 10)))
    for s in [2.0, 3.0]:
        grid.append(("iso", N_DEF, 128, s, 500 + int(s * 10)))
    for s in [2.0, 3.0]:
        grid.append(("iso", 500, D_DEF, s, 600 + int(s * 10)))

    corpora = [_corpus(f, N, D, s, seed) for (f, N, D, s, seed) in grid]
    corpora.sort(key=lambda c: c["rho"])
    rho = [c["rho"] for c in corpora]
    recall = [c["recall"] for c in corpora]
    m_t = [c["m_t_raw"] for c in corpora]

    # vacuity: interpolate rho where recall crosses 0.5 (corpora sorted by rho ascending)
    rho50, bracketed = None, False
    for i in range(len(corpora) - 1):
        r0, r1 = recall[i], recall[i + 1]
        if (r0 - 0.5) * (r1 - 0.5) <= 0 and r0 != r1:
            w = (0.5 - r0) / (r1 - r0)
            rho50 = rho[i] + w * (rho[i + 1] - rho[i])
            bracketed = True
            break

    sp_rho = _spearman(rho, recall)
    sp_base = _spearman(m_t, recall)
    hi_ok = all(c["recall"] >= 0.8 for c in corpora if c["rho"] >= 1.2)
    lo_ok = all(c["recall"] <= 0.2 for c in corpora if c["rho"] <= 0.83)

    verdict = {
        "n_corpora": bool(len(corpora) >= 8),
        "sweep_brackets_recall50": bool(bracketed),
        "ordering": bool(sp_rho >= 0.90),
        "vacuity_locates_death": bool(bracketed and abs(np.log(rho50)) <= np.log(1.20)),
        "sharp_separation": bool(hi_ok and lo_ok),
        "beats_baseline": bool(sp_rho > sp_base),
    }
    out = {
        "claim": "GO-3 certificate vacuity v2", "prereg": "GO-P-2026-013",
        "n_corpora": len(corpora),
        "spearman_rho_recall": sp_rho, "spearman_baseline_mt_recall": sp_base,
        "rho_at_recall50": rho50, "recall50_bracketed": bracketed,
        "hi_band_ok": hi_ok, "lo_band_ok": lo_ok,
        "corpora": [{k: c[k] for k in ("family", "N", "D", "sigma", "rho", "mu_hat", "mu_crit", "recall", "top10")} for c in corpora],
        "verdict": verdict,
    }
    out["GO3_supported"] = all(verdict.values())
    print("===GO3-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
