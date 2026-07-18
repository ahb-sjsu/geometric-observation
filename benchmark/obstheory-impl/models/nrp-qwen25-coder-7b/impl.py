import numpy as np

def solve(M, theta0_deg, kappa, s0sq_list, n_trials, seed):
    np.random.seed(seed)
    theta0 = np.deg2rad(theta0_deg)
    a = np.exp(1j * np.pi * np.arange(M) * np.sin(theta0))
    w_hat = np.array([np.cos(theta0), np.sin(theta0)])
    w_hat = w_hat / np.linalg.norm(w_hat)
    w_hat_real = np.array([w_hat[0], 0, w_hat[1], 0])

    mse = {"invariant": [], "recon": [], "anti": []}
    recon_energy = {"invariant": [], "recon": [], "anti": []}

    for s0sq in s0sq_list:
        s = np.exp(1j * np.random.randn())
        delta_invariant = np.random.randn(2) * np.sqrt(s0sq / kappa)
        delta_recon = np.random.randn(2 * M) * np.sqrt(s0sq)
        delta_anti = np.random.randn(2) * np.sqrt(s0sq * kappa)

        x_invariant = a * s + delta_invariant @ w_hat_real
        x_recon = a * s + delta_recon
        x_anti = a * s + delta_anti @ w_hat_real

        theta_hat_invariant = np.argmax(np.abs(np.dot(a.conj().T, x_invariant))**2)
        theta_hat_recon = np.argmax(np.abs(np.dot(a.conj().T, x_recon))**2)
        theta_hat_anti = np.argmax(np.abs(np.dot(a.conj().T, x_anti))**2)

        mse["invariant"].append((theta_hat_invariant - theta0)**2 * (180 / np.pi)**2)
        mse["recon"].append((theta_hat_recon - theta0)**2 * (180 / np.pi)**2)
        mse["anti"].append((theta_hat_anti - theta0)**2 * (180 / np.pi)**2)

        recon_energy["invariant"].append(np.linalg.norm(delta_invariant)**2)
        recon_energy["recon"].append(np.linalg.norm(delta_recon)**2)
        recon_energy["anti"].append(np.linalg.norm(delta_anti)**2)

    omission_floor_mult = mse["invariant"][-1] / mse["invariant"][-1]
    shuffled_flip = 0

    return {
        "read_dir": w_hat_real.tolist(),
        "mse": mse,
        "recon_energy": recon_energy,
        "omission_floor_mult": omission_floor_mult,
        "shuffled_flip": shuffled_flip,
    }
