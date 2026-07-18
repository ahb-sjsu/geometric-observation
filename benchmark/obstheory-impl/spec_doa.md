# ObsTheory-Impl benchmark — DOA task specification

You are given a problem in array signal processing. Implement it in Python and return the
requested measurements. **You are graded on a hidden oracle**; do not look for reference
solutions. Derive what you need from this specification alone.

## Physical setup
A single narrowband source impinges on an **M-element uniform linear array** (ULA) with
half-wavelength spacing. The complex array snapshot is
```
x = a(theta0) * s + delta        (x in C^M)
```
where the steering vector is `a_m(theta) = exp(1j * pi * m * sin(theta))` for `m = 0..M-1`
(half-wavelength ⇒ the per-element phase is `pi*m*sin(theta)`), `s` is the source amplitude
(take |s| = 1), and `delta` is additive **compression error** you will shape below.

## The downstream consumer
A consumer `C` estimates the source angle `theta` from `x`. Implement a reasonable
**continuous** angle estimator — e.g. matched-filter / beamformer maximum-likelihood: maximize
`|a(theta)^H x|^2` over `theta`, refined to continuous precision (Newton or a fine local
search — NOT a coarse grid pick). The downstream distortion is the squared angle error
`(theta_hat - theta0)^2` in **degrees^2**.

## The compression protocol — three arms at matched rate
Work in the real embedding `C^M ≅ R^{2M}` via `v = [Re(z); Im(z)]`. The compression error's
covariance is **diagonal in an orthonormal basis of R^{2M} whose first axis is the
"informative direction"** `w_hat` — the unit real vector along which a measurement
perturbation most changes the angle estimate. **You must determine `w_hat` yourself** from the
consumer above (it is a property of the array geometry at `theta0`).

Given a base variance `s0^2` and a per-step ratio `kappa > 1`, define three arms at **matched
total log-precision** (identical rate: `sum_i log(1/var_i)` equal across arms), with `dR = 1`
informative dim and `dP = 2M-1` complement dims:
- **invariant**: var on `w_hat` = `s0^2 / kappa`; complement var = `s0^2 * kappa^(1/dP)`.
- **recon**: var = `s0^2` on all `2M` dims (this minimizes `E||delta||^2`).
- **anti**: var on `w_hat` = `s0^2 * kappa`; complement var = `s0^2 * kappa^(-1/dP)`.

For each arm and each `s0^2` in the sweep, Monte-Carlo over `n_trials`: draw `delta` with the
shaped covariance (in the `w_hat`-first basis), form `x_hat = x + delta`, estimate `theta_hat`,
and record `(theta_hat - theta0)^2` [deg^2] and `||delta||^2`.

## Also measure
- **omission**: an arm identical to `invariant` but with `w_hat` left **UNCODED** — fixed
  variance `0.05` on `w_hat` regardless of `s0^2`. Report `omission_floor_mult` = its MSE at the
  **highest** rate divided by the coded `invariant` MSE at the highest rate.
- **shuffled control**: repeat the three-arm sweep but shape around a **random** unit direction
  instead of `w_hat`. Report `shuffled_flip` = the flip count (see below) over the sweep.

## Deliverable — a Python module `impl.py` exposing exactly:
```python
def solve(M, theta0_deg, kappa, s0sq_list, n_trials, seed):
    # returns a dict:
    return {
      "read_dir": [...],            # your unit w_hat in R^{2M} ([Re; Im] order) at theta0, length 2M
      "mse": {"invariant": [...], "recon": [...], "anti": [...]},           # one float per s0sq, deg^2
      "recon_energy": {"invariant": [...], "recon": [...], "anti": [...]},  # one float per s0sq
      "omission_floor_mult": 0.0,   # float
      "shuffled_flip": 0,           # int in 0..len(s0sq_list)
    }
```
Constraints: **pure numpy + stdlib**, deterministic given `seed`, no file or network access.
`theta0_deg` is in degrees; convert internally. Lists in `mse`/`recon_energy` are ordered to
match `s0sq_list`.

## "The flip" (for your own sanity check; the oracle checks it independently)
angle MSE `invariant <= recon <= anti` at every rate, **and** `recon` has the smallest
reconstruction energy at every rate. If your `w_hat` is wrong, your arms are shaped wrong and
this will not hold.
