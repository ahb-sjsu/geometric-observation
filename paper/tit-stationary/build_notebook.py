"""Writes reproduce.ipynb.  Run:  python build_notebook.py
then:  jupyter nbconvert --to notebook --execute reproduce.ipynb --output reproduce-executed.ipynb
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell

nb.cells = [
    md("# Rate, Leakage, and Distortion for Stationary Gaussian Sources — reproduction\n\n"
       "This notebook reruns every numerical check quoted in the manuscript (`tit-stationary.tex`), "
       "prints the tables of Section IX, shows the recorded distortion sweep, and draws Fig. 1. It needs only `numpy` and `matplotlib`. "
       "All random instances come from one fixed seed, so the numbers are deterministic up to "
       "floating-point differences between BLAS builds.\n\n"
       "No proof in the paper depends on these numbers; they check the statements independently of the derivations."),
    code("import json, sys, platform\nimport numpy as np\nimport spectral_core as sc\nimport verify_spectral as vs\n"
         "print('python', sys.version.split()[0], '| numpy', np.__version__, '|', platform.platform())\nprint('seed', vs.SEED)"),
    md("## 1. Run all checks\n\nEach line is one statement of the paper. `PASS` means the stated tolerance was met. "
       "This cell takes a few minutes: it solves window problems of dimension up to 96 with a solver that assumes no structure."),
    code("status = vs.main()\nout = vs.OUT\nassert status == 0, out['_meta']['failed']"),
    md("## 2. Theorem 3 — the period-$n$ problem splits over Fourier frequencies\n\n"
       "The full real $pn$-dimensional program, solved with no structure assumed, against the per-frequency "
       "Hermitian programs with one common level."),
    code("r = out['thm1_decoupling']\nfor k in ('cases', 'cost', 'X', 'kkt', 'offdiag'):\n    print(f'{k:>8}: {r[k]:.3g}')"),
    md("## 3. Theorem 4 — convergence to the spectral region (Table I, left)"),
    code("print(' alpha     n   |V_n - V| (bits)      level nu')\n"
         "for row in out['thm2_limit']['table']:\n"
         "    print(f\"{row['alpha']:6.1f} {row['n']:5d}   {row['err']:.3e}        {row['nu']:.8f}\")"),
    md("## 4. Theorem 5 and Corollary 6 — the scalar pair, and disjoint bands (Fig. 1)"),
    code("print({k: out['thm3_scalar_closed_form'][k] for k in ('val', 'alloc', 'thr')})\n"
         "b = out['cor_disjoint_bands']\nprint({k: b[k] for k in b if k not in ('ok', 'seconds')})\n"
         "print('leakage factor', round(b['L_of_rate_opt'] / b['L_min'], 2), '| rate factor', round(b['R_of_leak_opt'] / b['R_min'], 2))"),
    code("%matplotlib inline\nimport plot_bands\nfig = plot_bands.main()"),
    md("### Distortion sweep (Table II)\n\nThe sweep takes about twelve minutes, so this cell shows the recorded "
       "`sweep_bands.json`. Set `RERUN_SWEEP = True` to recompute it with `sweep_bands.py`."),
    code("RERUN_SWEEP = False\nimport sweep_bands\nsw = sweep_bands.main() if RERUN_SWEEP else json.load(open('sweep_bands.json'))\n"
         "print(' D/Dmax  rate  leak  both    R_min    L_min   L-factor R-factor')\n"
         "for r in sw['rows']:\n"
         "    print(f\"{r['frac']:7.2f} {r['bands_rate']:5d} {r['bands_leak']:5d} {r['overlap']:5d}   {r['R_min']:.4f}   {r['L_min']:.4f}    {r['leak_factor']:.2f}     {r['rate_factor']:.2f}\")\n"
         "print('supports disjoint for D/Dmax >=', round(sw['onset_hi'], 4), '| overlap at', round(sw['onset_lo'], 4))"),
    md("## 5. Proposition 7 — a delay changes nothing"),
    code("print(out['prop_delay_invariance'])"),
    md("## 6. Theorems 10 and 15 — windows of the stationary source (Table I, right)\n\n"
       "Affine spectrum: exact splitting in the Toeplitz eigenbasis and convergence. "
       "General spectrum: the computed gap, which Theorem 15 says is nonnegative and tends to zero."),
    code("print('affine spectrum:  N  alpha   window cost    gap (bits)    N*gap')\n"
         "for row in out['thm4_affine_toeplitz']['table']:\n"
         "    print(f\"{row['n']:20d} {row['alpha']:5.1f}   {row['cost_eig']:.8f}   {row['gap']:+.3e}   {row['n_gap']:+.4f}\")\n"
         "print('exact-splitting error', out['thm4_affine_toeplitz']['decoupling_err'])\n"
         "print()\nprint('general spectrum: alpha  N   window cost    gap (bits)    N*gap')\n"
         "for row in out['conj1_general_toeplitz_evidence']['table']:\n"
         "    print(f\"{row['alpha']:22.1f} {row['n']:3d}   {row['cost']:.8f}   {row['gap']:+.3e}   {row['n_gap']:+.4f}\")"),
    md("## 6b. Theorem 16 — covariance steps of the achievability proof\n\n"
       "The coding theorem is not something a computation verifies. This checks the steps of its proof that are "
       "statements about covariances: the decomposition, block independence, the coupling, and the two leakage inequalities."),
    code("import verify_achievability as va\nassert va.main() == 0"),
    md("## 6c. Theorem 15 — steps of the proof of the window theorem\n\n"
       "Unwhitened form, order sandwich, subadditivity, finite-memory embedding, sign of the gap, "
       "the block-Toeplitz feasible point, and both bounds on the gap. About a minute."),
    code("import verify_windows as vw\nassert vw.main() == 0\n"
         "for r in vw.OUT['toeplitz_point_and_bound']['table']:\n"
         "    print(f\"alpha={r['alpha']:.1f} N={r['N']:3d}  gap={r['gap_window']:.4e}  "
         "first bound={r['bound_s']:.4e}  explicit bound={r['bound']:.3e}\")"),
    md("## 7. Proposition 8 — what the holder keeps"),
    code("r = out['prop_retention']\nfor k in r:\n    if k not in ('ok', 'seconds'):\n        print(f'{k:>22}: {r[k]:.10g}')\n"
         "rho2, Dn = 0.64, 0.4\nfor name in ('q_slice', 'q_prefix0', 'q_prefix3', 'q_path'):\n"
         "    q = r[name]\n    print(name, 'leakage (bits):', round(float(sc.ell_scalar(rho2, 1 / (1 - q), Dn)), 4))\n"
         "print('rate (no holder):', round(0.5 * np.log2(1 / Dn), 4))"),
    md("## 8. Summary"),
    code("m = out['_meta']\nprint('failed:', m['failed'], '| seconds:', m['seconds'])\n"
         "print('all checks passed' if not m['failed'] else 'FAILURES')"),
]
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}
nbf.write(nb, "reproduce.ipynb")
print("wrote reproduce.ipynb")
