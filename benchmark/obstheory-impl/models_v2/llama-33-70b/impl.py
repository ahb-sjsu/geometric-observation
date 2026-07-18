import numpy as np

def solve(M, theta0_deg, kappa, s0sq_list, n_trials, seed):
    np.random.seed(seed)
    theta0 = np.deg2rad(theta0_deg)
    w_hat = np.zeros(2 * M)
    for m in range(M):
        w_hat[2 * m] = np.cos(np.pi * m * np.sin(theta0))
        w_hat[2 * m + 1] = np.sin(np.pi * m * np.sin(theta0))
    w_hat /= np.linalg.norm(w_hat)

    mse = {"invariant": [], "recon": [], "anti": []}
    recon_energy = {"invariant": [], "recon": [], "anti": []}
    omission_floor_mult = 0.0
    shuffled_flip = 0

    for s0sq in s0sq_list:
        invariant_var = s0sq / kappa
        invariant_complement_var = s0sq * kappa ** (1 / (2 * M - 1))
        recon_var = s0sq
        anti_var = s0sq * kappa
        anti_complement_var = s0sq * kappa ** (-1 / (2 * M - 1))

        invariant_mse = 0
        recon_mse = 0
        anti_mse = 0
        invariant_energy = 0
        recon_energy_val = 0
        anti_energy = 0

        for _ in range(n_trials):
            s = np.random.uniform(-1, 1) + 1j * np.random.uniform(-1, 1)
            s /= np.abs(s)
            x = np.zeros(2 * M, dtype=np.float64)
            for m in range(M):
                x[2 * m] = np.cos(np.pi * m * np.sin(theta0)) * np.real(s)
                x[2 * m + 1] = np.sin(np.pi * m * np.sin(theta0)) * np.real(s)

            # Invariant arm
            delta = np.random.normal(0, np.sqrt(invariant_complement_var), size=2 * M)
            delta -= np.dot(delta, w_hat) * w_hat
            delta += np.random.normal(0, np.sqrt(invariant_var), size=1) * w_hat
            x_hat = x + delta
            theta_hat = np.arcsin(np.sum(x_hat[:2 * M:2] * w_hat[:2 * M:2] + x_hat[1:2 * M:2] * w_hat[1:2 * M:2]) / np.linalg.norm(x_hat))
            invariant_mse += (np.rad2deg(theta_hat - theta0)) ** 2
            invariant_energy += np.sum(delta ** 2)

            # Recon arm
            delta = np.random.normal(0, np.sqrt(recon_var), size=2 * M)
            x_hat = x + delta
            theta_hat = np.arcsin(np.sum(x_hat[:2 * M:2] * w_hat[:2 * M:2] + x_hat[1:2 * M:2] * w_hat[1:2 * M:2]) / np.linalg.norm(x_hat))
            recon_mse += (np.rad2deg(theta_hat - theta0)) ** 2
            recon_energy_val += np.sum(delta ** 2)

            # Anti arm
            delta = np.random.normal(0, np.sqrt(anti_complement_var), size=2 * M)
            delta -= np.dot(delta, w_hat) * w_hat
            delta += np.random.normal(0, np.sqrt(anti_var), size=1) * w_hat
            x_hat = x + delta
            theta_hat = np.arcsin(np.sum(x_hat[:2 * M:2] * w_hat[:2 * M:2] + x_hat[1:2 * M:2] * w_hat[1:2 * M:2]) / np.linalg.norm(x_hat))
            anti_mse += (np.rad2deg(theta_hat - theta0)) ** 2
            anti_energy += np.sum(delta ** 2)

            # Omission arm
            if s0sq == max(s0sq_list):
                delta = np.random.normal(0, np.sqrt(0.05), size=1) * w_hat
                delta += np.random.normal(0, np.sqrt(invariant_complement_var), size=2 * M)
                delta -= np.dot(delta, w_hat) * w_hat
                x_hat = x + delta
                theta_hat = np.arcsin(np.sum(x_hat[:2 * M:2] * w_hat[:2 * M:2] + x_hat[1:2 * M:2] * w_hat[1:2 * M:2]) / np.linalg.norm(x_hat))
                omission_floor_mult = (np.rad2deg(theta_hat - theta0)) ** 2 / (invariant_mse / n_trials)

            # Shuffled arm
            shuffled_w_hat = np.random.normal(0, 1, size=2 * M)
            shuffled_w_hat /= np.linalg.norm(shuffled_w_hat)
            delta = np.random.normal(0, np.sqrt(invariant_complement_var), size=2 * M)
            delta -= np.dot(delta, shuffled_w_hat) * shuffled_w_hat
            delta += np.random.normal(0, np.sqrt(invariant_var), size=1) * shuffled_w_hat
            x_hat = x + delta
            theta_hat = np.arcsin(np.sum(x_hat[:2 * M:2] * shuffled_w_hat[:2 * M:2] + x_hat[1:2 * M:2] * shuffled_w_hat[1:2 * M:2]) / np.linalg.norm(x_hat))
            if (np.rad2deg(theta_hat - theta0)) ** 2 > invariant_mse / n_trials:
                shuffled_flip += 1

        mse["invariant"].append(invariant_mse / n_trials)
        mse["recon"].append(recon_mse / n_trials)
        mse["anti"].append(anti_mse / n_trials)
        recon_energy["invariant"].append(invariant_energy / n_trials)
        recon_energy["recon"].append(recon_energy_val / n_trials)
        recon_energy["anti"].append(anti_energy / n_trials)

    return {
        "read_dir": w_hat.tolist(),
        "mse": mse,
        "recon_energy": recon_energy,
        "omission_floor_mult": omission_floor_mult,
        "shuffled_flip": shuffled_flip,
    }