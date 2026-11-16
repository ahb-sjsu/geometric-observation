"""Writes reproduce.ipynb.  Run:  python build_notebook.py
then:  jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=7200 \
           reproduce.ipynb --output reproduce-executed.ipynb
The executed notebook takes about forty minutes. It needs numpy, scipy, mpmath,
matplotlib, nbformat, nbclient and ipykernel.
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell

nb.cells = [
    md("# Rate, Leakage, and Distortion Beyond Stationary Gaussian Sources: reproduction\n\n"
       "This notebook reruns every numerical check quoted in the manuscript (`tit-beyond-stationary.tex`), "
       "prints the numbers of its Appendix A, and recomputes the worked example and Fig. 1. It needs `numpy`, "
       "`scipy`, `mpmath` and `matplotlib`, and the solver `spectral_core.py` of the companion paper in "
       "`../tit-stationary/`. "
       "All random instances come from one fixed seed, so the numbers are deterministic up to floating-point "
       "differences between BLAS builds.\n\n"
       "No proof in the paper depends on these numbers. They check single-letter and spectral quantities. "
       "The coding theorems themselves are not something a computation verifies.\n\n"
       "Running everything takes about forty minutes: about one minute for Section 1, fifteen for Section 2, "
       "twelve for Section 4, and under a minute for Section 5."),
    code("import json, sys, platform, time\nimport numpy as np\n"
         "print('python', sys.version.split()[0], '| numpy', np.__version__, '|', platform.platform())"),

    md("## 1. Sources that are not Gaussian (Section III)\n\n"
       "A source in $\\mathbb R^2$ that is a mixture of four Gaussian components. Entropies are computed by "
       "Gauss-Hermite quadrature on each component. Checks: the Gaussian test channel has rate and leakage below "
       "the Gaussian values (Theorem 2); the weighted cost is above the lower bound (Theorem 3), also for a channel "
       "with mixture noise; the gap to the lower bound vanishes with the distortion (Theorem 5); the mixing "
       "inequality (Corollary 6)."),
    code("import verify_nongauss as vn\nassert vn.main() == 0\nng = vn.OUT"),
    code("d = ng['deficits']\nprint('deficit of the source, bits:', round(d['D_T'], 4))\n"
         "print('conditional deficit, Gaussian noise:', round(d['delta_gauss_noise'], 4), "
         "'| mixture noise:', round(d['delta_mixture_noise'], 4))\n"
         "print()\nprint('noise    alpha  D/Dmax   rate   Gauss rate   leak   Gauss leak   lower    cost    upper')\n"
         "for r in ng['inner']['table']:\n"
         "    print(f\"{r['noise']:8s} {r['alpha']:4.1f}  {r['D_over_Dmax']:5.2f}  {r['rate']:7.4f}  {r['rate_gauss']:7.4f}   "
         "{r['leak']:7.4f}  {r['leak_gauss']:7.4f}   {r['lower']:7.4f} {r['cost']:7.4f} {r['upper']:7.4f}\")"),
    code("print('gap between the Gaussian channel and the lower bound, bits, as D -> 0')\n"
         "print('D/Dmax = 0.5, 0.2, 0.05, 0.01, 0.002, 0.0004')\n"
         "for r in ng['high_resolution']['table']:\n"
         "    print('alpha', r['alpha'], [round(float(g), 5) for g in r['gaps']])"),

    md("## 2. Locally stationary sources (Sections V and VI)\n\n"
       "Time-varying moving averages with a white floor (Proposition 15). Checks: condition (L2); the frontier "
       "cost of the whole window against the time-frequency cost (Theorem 13); the cost of frozen spectra; the "
       "inequality inside Lemma 10 with the exact information between blocks; the comparison of frontier costs "
       "that Lemma 11 implies; Corollary 16; the three facts (F1) to (F3) used by Proposition 14. "
       "About fifteen minutes."),
    code("import verify_ls as vl\nassert vl.main() == 0\nls = vl.OUT"),
    code("print('(L2): largest operator-norm distance of a block covariance from the local Toeplitz matrix')\n"
         "for r in ls['local_closeness']['table']:\n"
         "    print(f\"  block fraction {r['block_fraction']:.5f}   distance {r['max_op_distance']:.4f}\")\n"
         "print()\nprint('window frontier cost minus the time-frequency cost, bits')\n"
         "for r in ls['window_to_ls']['table']:\n"
         "    print(f\"  {r['source']:6s} alpha={r['alpha']:.1f}  N={r['N']}  gaps={[round(float(g), 5) for g in r['gaps']]}\")\n"
         "print()\nprint('frozen spectra, B = 2, 4, 8, 16: cost minus the time-frequency cost, bits')\n"
         "for r in ls['riemann']['table']:\n"
         "    print('  alpha', r['alpha'], [round(float(g), 5) for g in r['gaps']])"),

    md("## 3. The worked example and Fig. 1 (Section VI)\n\n"
       "The source in $\\mathbb R^2$ of the example after Proposition 15, at $D = 0.35 D_{\\max}$: the two optimal "
       "descriptions, the window costs, and the stationary source with the time-averaged spectrum."),
    code("import example_ls\nassert example_ls.main() == 0\nex = json.load(open('example_ls.json'))"),
    code("from IPython.display import Image\nImage('fig_ls.png', width=900)"),

    md("## 4. Cyclostationary sources and independent regimes (Sections VII and VIII)\n\n"
       "Periodic moving averages. Checks: the harmonic form (Proposition 19); the stacked cost of a stationary "
       "source (Corollary 20); the starting phase and the window costs (Theorem 18); independent regimes "
       "(Proposition 23); the phase-averaged spectrum (Theorem 22). About twelve minutes."),
    code("import verify_cyclo as vc\nassert vc.main() == 0\ncy = vc.OUT"),
    code("print('window cost minus the stacked spectral cost, N = 6, 12, 24, 48, 96, bits')\n"
         "for r in cy['window_converse']['table']:\n"
         "    print('  alpha', r['alpha'], [round(float(g), 6) for g in r['gaps']])\n"
         "print()\nprint('one instance: cyclostationary cost against the phase-averaged spectrum')\n"
         "for r in cy['stationarized_report']['table']:\n"
         "    print(f\"  alpha={r['alpha']:.1f} D/Dmax={r['D_over_Dmax']:.1f}  {r['cyclostationary']:.5f}  "
         "{r['stationarized']:.5f}  saving {r['saving']:+.5f}\")"),

    md("## 5. Unstable autoregressive sources (Section IX)\n\n"
       "Four scalar Gaussian autoregressive sources with unstable poles, started from zero: one pole at 1.5; "
       "poles at 1.3 and 0.5; poles at 1.2 and -1.4; a complex pair of modulus 1.15. The holder sees each symbol "
       "through one gain in white noise, with $H = 1$ and $H = 0$. Window sizes $N = 40, 80, 160, 320$. "
       "Checks: the split of the window covariance into at most $d$ exceptional eigenvalues and a bulk, the "
       "log-sum of the exceptional ones against $2N\\rho_\\star$, and the law of the bulk (Lemma 25); the window "
       "cost against the limit of Theorem 26; that feasible error covariances have eigenvalues below those of "
       "the source (Lemma 24); that one allocation $\\delta = \\min\\{\\lambda, \\theta\\}$ is optimal at every "
       "weight (Lemma 24, Corollary 27); the determinant identity against an 80-digit computation. The limits are "
       "checked at the $1/N$ rate the proofs give, not at a fixed tolerance; the paper's README says why."),
    code("import verify_unstable as vu\nassert vu.main() == 0\nun = vu.OUT"),
    code("print('instability rate rho* (bits) and N times the error at N = 320')\n"
         "for name, c in un['cases'].items():\n"
         "    e = c['N_times_err_last']\n"
         "    print(f\"  {name:18s} rho* = {c['rbar_bits']:.4f}   log-sum: {e['outlier']:+.4f}   cost: {e['cost_gap']:+.4f}\")\n"
         "print()\nprint('largest |window cost - limit of Theorem 26|, bits, N = 40, 80, 160, 320')\n"
         "for name, c in un['cases'].items():\n"
         "    print(f\"  {name:18s}\", [round(float(max(abs(v['gap']) for v in r['costs'].values())), 5) for r in c['rows']])\n"
         "print()\nprint('common optimizer: largest difference from delta = min(lambda, theta), bits:', "
         "f\"{un['common_optimizer']['max_diff']:.1e}\")\n"
         "print('determinant identity, relative difference from 80 digits:', "
         "[f\"{r['rel_diff']:.1e}\" for r in un['mp_check']['rows']])"),

    md("## 6. Summary\n\n"
       "Formal verification is separate from this notebook. The Lean 4 module "
       "`lean/ObservationTheory/BeyondStationary.lean` checks fifteen algebraic steps of the proofs, and "
       "`lean/ObservationTheory/LogDet.lean` has the matrix concavity used in Theorem 3. Their build record is "
       "`lean-beyond-2026-11-16.txt` in this folder."),
    code("total = 0\n# verify_unstable keeps its verdicts per source, so it is counted after this loop\n"
         "for name, out in (('verify_nongauss', ng), ('verify_ls', ls), ('verify_cyclo', cy)):\n"
         "    m = out['_meta']\n"
         "    n = sum(1 for k, v in out.items() if k != '_meta' and isinstance(v, dict) and 'ok' in v)\n"
         "    p = sum(1 for k, v in out.items() if k != '_meta' and isinstance(v, dict) and v.get('ok'))\n"
         "    total += n - p\n"
         "    print(f\"{name:16s} {p} of {n} entries ok | failed: {m['failed']} | seconds: {m['seconds']}\")\n"
         "flags = [v for c in un['cases'].values() for v in c['verdict'].values()]\n"
         "flags += [un[k]['ok'] for k in ('feasible_spectra_dominated', 'common_optimizer', 'mp_check')]\n"
         "total += flags.count(False)\n"
         "print(f\"{'verify_unstable':16s} {flags.count(True)} of {len(flags)} entries ok | failed: "
         "{un['_meta']['failed']} | seconds: {un['_meta']['seconds']}\")\n"
         "print('all checks passed' if total == 0 else 'FAILURES')\nassert total == 0"),
]
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}
nbf.write(nb, "reproduce.ipynb")
print("wrote reproduce.ipynb")
