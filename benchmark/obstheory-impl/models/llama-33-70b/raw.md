```python
import numpy as np

def solve(M, theta0_deg, kappa, s0sq_list, n_trials, seed):
    np.random.seed(seed)
    
    # Convert theta0 to radians
    theta0 = np.deg2rad(theta0_deg)
    
    # Steering vector
    m = np.arange(M)
    a = np.exp(1j * np.pi * m * np.sin(theta0))
    
    # Informative direction w_hat
    w_hat = np.concatenate((np.cos(np.pi * m * np.sin(theta0)), np.sin(np.pi * m * np.sin(theta0))))
    w_hat = w_hat / np.linalg.norm(w_hat)
    
    # Initialize results
    mse = {"invariant": [], "recon": [], "anti": []}
    recon_energy = {"invariant": [], "recon": [], "anti": []}
    omission_floor_mult = 0.0
    shuffled_flip = 0
    
    # Sweep over s0sq_list
    for s0sq in s0sq_list:
        # Invariant arm
        var_inv = s0sq / kappa
        var_comp = s0sq * kappa ** (1 / (2 * M - 1))
        cov_inv = np.diag(np.concatenate(([var_inv], [var_comp] * (2 * M - 1))))
        delta_inv = np.random.multivariate_normal(np.zeros(2 * M), cov_inv, n_trials)
        delta_inv = delta_inv @ np.linalg.inv(np.eye(2 * M)[:, np.argsort(np.abs(w_hat))])
        x_hat_inv = np.concatenate((np.cos(np.pi * m * np.sin(theta0)), np.sin(np.pi * m * np.sin(theta0)))) + delta_inv
        theta_hat_inv = np.arcsin(np.sum(x_hat_inv[:, :M] * np.cos(np.pi * m * np.sin(theta0)) + x_hat_inv[:, M:] * np.sin(np.pi * m * np.sin(theta0)), axis=1) / np.linalg.norm(x_hat_inv, axis=1))
        mse["invariant"].append(np.mean((np.rad2deg(theta_hat_inv) - theta0_deg) ** 2))
        recon_energy["invariant"].append(np.mean(np.sum(delta_inv ** 2, axis=1)))
        
        # Recon arm
        cov_recon = np.eye(2 * M) * s0sq
        delta_recon = np.random.multivariate_normal(np.zeros(2 * M), cov_recon, n_trials)
        x_hat_recon = np.concatenate((np.cos(np.pi * m * np.sin(theta0)), np.sin(np.pi * m * np.sin(theta0)))) + delta_recon
        theta_hat_recon = np.arcsin(np.sum(x_hat_recon[:, :M] * np.cos(np.pi * m * np.sin(theta0)) + x_hat_recon[:, M:] * np.sin(np.pi * m * np.sin(theta0)), axis=1) / np.linalg.norm(x_hat_recon, axis=1))
        mse["recon"].append(np.mean((np.rad2deg(theta_hat_recon) - theta0_deg) ** 2))
        recon_energy["recon"].append(np.mean(np.sum(delta_recon ** 2, axis=1)))
        
        # Anti arm
        var_anti = s0sq * kappa
        var_comp = s0sq * kappa ** (-1 / (2 * M - 1))
        cov_anti = np.diag(np.concatenate(([var_anti], [var_comp] * (2 * M - 1))))
        delta_anti = np.random.multivariate_normal(np.zeros(2 * M), cov_anti, n_trials)
        delta_anti = delta_anti @ np.linalg.inv(np.eye(2 * M)[:, np.argsort(np.abs(w_hat))])
        x_hat_anti = np.concatenate((np.cos(np.pi * m * np.sin(theta0)), np.sin(np.pi * m * np.sin(theta0)))) + delta_anti
        theta_hat_anti = np.arcsin(np.sum(x_hat_anti[:, :M] * np.cos(np.pi * m * np.sin(theta0)) + x_hat_anti[:, M:] * np.sin(np.pi * m * np.sin(theta0)), axis=1) / np.linalg.norm(x_hat_anti, axis=1))
        mse["anti"].append(np.mean((np.rad2deg(theta_hat_anti) - theta0_deg) ** 2))
        recon_energy["anti"].append(np.mean(np.sum(delta_anti ** 2, axis=1)))
        
        # Omission arm
        if s0sq == s0sq_list[-1]:
            var_omission = 0.05
            cov_omission = np.diag(np.concatenate(([var_omission], [s0sq] * (2 * M - 1))))
            delta_omission = np.random.multivariate_normal(np.zeros(2 * M), cov_omission, n_trials)
            delta_omission = delta_omission @ np.linalg.inv(np.eye(2 * M)[:, np.argsort(np.abs(w_hat))])
            x_hat_omission = np.concatenate((np.cos(np.pi * m * np.sin(theta0)), np.sin(np.pi * m * np.sin(theta0)))) + delta_omission
            theta_hat_omission = np.arcsin(np.sum(x_hat_omission[:, :M] * np.cos(np.pi * m * np.sin(theta0)) + x_hat_omission[:, M:] * np.sin(np.pi * m * np.sin(theta0)), axis=1) / np.linalg.norm(x_hat_omission, axis=1))
            omission_floor_mult = np.mean((np.rad2deg(theta_hat_omission) - theta0_deg) ** 2) / mse["invariant"][-1]
        
        # Shuffled control
        w_hat_shuffled = np.random.rand(2 * M)
        w_hat_shuffled = w_hat_shuffled / np.linalg.norm(w_hat_shuffled)
        var_shuffled = s0sq / kappa
        var_comp = s0sq * kappa ** (1 / (2 * M - 1))
        cov_shuffled = np.diag(np.concatenate(([var_shuffled], [var_comp] * (2 * M - 1))))
        delta_shuffled = np.random.multivariate_normal(np.zeros(2 * M), cov_shuffled, n_trials)
        delta_shuffled = delta_shuffled @ np.linalg.inv(np.eye(2 * M)[:, np.argsort(np.abs(w_hat_shuffled))])
        x_hat_shuffled = np.concatenate((np.cos(np.pi * m * np.sin(theta0)), np.sin(np.pi * m * np.sin(theta0)))) + delta_shuffled
        theta_hat_shuffled = np.arcsin(np.sum(x_hat_shuffled[:, :M] * np.cos(np.pi * m * np.sin(theta0)) + x_hat_shuffled[:, M:] * np.sin(np.pi * m * np.sin(theta0)), axis=1) / np.linalg.norm(x_hat_shuffled, axis=1))
        if np.mean((np.rad2deg(theta_hat_shuffled) - theta0_deg) ** 2) < mse["invariant"][-1]:
            shuffled_flip += 1
    
    return {
        "read_dir": w_hat,
        "mse": mse,
        "recon_energy": recon_energy,
        "omission_floor_mult": omission_floor_mult,
        "shuffled_flip": shuffled_flip,
    }
```