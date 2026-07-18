import numpy as np

def solve(M, theta0_deg, kappa, s0sq_list, n_trials, seed):
    np.random.seed(seed)
    theta0 = np.deg2rad(theta0_deg)
    
    # Steering vector
    m = np.arange(M)
    a = np.exp(1j * np.pi * m * np.sin(theta0))
    x = a  # since |s| = 1
    
    # Convert to real embedding
    v = np.concatenate([np.real(x), np.imag(x)])
    
    # Consumer function: ML estimator via Newton's method
    def estimate_theta(x_hat):
        def objective(theta):
            a_theta = np.exp(1j * np.pi * m * np.sin(theta))
            return -np.abs(np.vdot(a_theta, x_hat))**2
        
        # Initial guess near theta0
        theta_hat = theta0
        for _ in range(10):  # Newton iterations
            # Numerical derivatives
            h = 1e-6
            f0 = objective(theta_hat)
            fp = objective(theta_hat + h)
            fm = objective(theta_hat - h)
            grad = (fp - fm) / (2 * h)
            hess = (fp - 2*f0 + fm) / (h**2)
            if np.abs(hess) < 1e-10:
                break
            delta = -grad/hess
            theta_hat += delta
            if np.abs(delta) < 1e-8:
                break
        return theta_hat
    
    # Compute w_hat (informative direction) via finite differences
    eps = 1e-6
    base_theta = estimate_theta(x)
    perturbations = []
    for i in range(2*M):
        dv = np.zeros(2*M)
        dv[i] = eps
        x_pert = x + (dv[:M] + 1j*dv[M:])
        theta_pert = estimate_theta(x_pert)
        sensitivity = (theta_pert - base_theta)/eps
        perturbations.append(sensitivity)
    w_hat = np.array(perturbations)
    w_hat /= np.linalg.norm(w_hat)
    
    # Basis with w_hat as first axis
    Q, _ = np.linalg.qr(w_hat.reshape(-1, 1))
    basis = np.column_stack([w_hat, Q[:, 1:]])
    
    # Monte Carlo simulations
    results = {
        "mse": {"invariant": [], "recon": [], "anti": []},
        "recon_energy": {"invariant": [], "recon": [], "anti": []},
    }
    
    for s0sq in s0sq_list:
        # Initialize accumulators
        mse_inv = 0.0
        mse_rec = 0.0
        mse_anti = 0.0
        energy_inv = 0.0
        energy_rec = 0.0
        energy_anti = 0.0
        
        for _ in range(n_trials):
            # Generate delta in the basis coordinates
            z = np.random.normal(0, 1, 2*M)
            
            # Invariant arm
            vars_inv = np.ones(2*M) * s0sq * kappa**(1/(2*M-1))
            vars_inv[0] = s0sq / kappa
            delta_basis_inv = z * np.sqrt(vars_inv)
            delta_inv = basis @ delta_basis_inv
            x_hat_inv = x + (delta_inv[:M] + 1j*delta_inv[M:])
            theta_hat_inv = estimate_theta(x_hat_inv)
            mse_inv += np.rad2deg(theta_hat_inv - theta0)**2
            energy_inv += np.sum(delta_inv**2)
            
            # Recon arm
            delta_basis_rec = z * np.sqrt(s0sq)
            delta_rec = basis @ delta_basis_rec
            x_hat_rec = x + (delta_rec[:M] + 1j*delta_rec[M:])
            theta_hat_rec = estimate_theta(x_hat_rec)
            mse_rec += np.rad2deg(theta_hat_rec - theta0)**2
            energy_rec += np.sum(delta_rec**2)
            
            # Anti arm
            vars_anti = np.ones(2*M) * s0sq * kappa**(-1/(2*M-1))
            vars_anti[0] = s0sq * kappa
            delta_basis_anti = z * np.sqrt(vars_anti)
            delta_anti = basis @ delta_basis_anti
            x_hat_anti = x + (delta_anti[:M] + 1j*delta_anti[M:])
            theta_hat_anti = estimate_theta(x_hat_anti)
            mse_anti += np.rad2deg(theta_hat_anti - theta0)**2
            energy_anti += np.sum(delta_anti**2)
        
        # Store averages
        results["mse"]["invariant"].append(mse_inv / n_trials)
        results["mse"]["recon"].append(mse_rec / n_trials)
        results["mse"]["anti"].append(mse_anti / n_trials)
        results["recon_energy"]["invariant"].append(energy_inv / n_trials)
        results["recon_energy"]["recon"].append(energy_rec / n_trials)
        results["recon_energy"]["anti"].append(energy_anti / n_trials)
    
    # Omission floor measurement
    s0sq_max = max(s0sq_list)
    mse_omission = 0.0
    mse_inv_max = results["mse"]["invariant"][-1]
    
    vars_omission = np.ones(2*M) * s0sq_max * kappa**(1/(2*M-1))
    vars_omission[0] = 0.05  # fixed variance on w_hat
    
    for _ in range(n_trials):
        z = np.random.normal(0, 1, 2*M)
        delta_basis_omission = z * np.sqrt(vars_omission)
        delta_omission = basis @ delta_basis_omission
        x_hat_omission = x + (delta_omission[:M] + 1j*delta_omission[M:])
        theta_hat_omission = estimate_theta(x_hat_omission)
        mse_omission += np.rad2deg(theta_hat_omission - theta0)**2
    
    omission_floor_mult = (mse_omission / n_trials) / mse_inv_max
    
    # Shuffled control
    shuffled_flip = 0
    random_dir = np.random.normal(0, 1, 2*M)
    random_dir /= np.linalg.norm(random_dir)
    Q_rand, _ = np.linalg.qr(random_dir.reshape(-1, 1))
    basis_rand = np.column_stack([random_dir, Q_rand[:, 1:]])
    
    prev_inv = None
    prev_rec = None
    prev_anti = None
    
    for s0sq in s0sq_list:
        mse_inv = 0.0
        mse_rec = 0.0
        mse_anti = 0.0
        
        for _ in range(n_trials):
            z = np.random.normal(0, 1, 2*M)
            
            # Invariant arm
            vars_inv = np.ones(2*M) * s0sq * kappa**(1/(2*M-1))
            vars_inv[0] = s0sq / kappa
            delta_basis_inv = z * np.sqrt(vars_inv)
            delta_inv = basis_rand @ delta_basis_inv
            x_hat_inv = x + (delta_inv[:M] + 1j*delta_inv[M:])
            theta_hat_inv = estimate_theta(x_hat_inv)
            mse_inv += np.rad2deg(theta_hat_inv - theta0)**2
            
            # Recon arm
            delta_basis_rec = z * np.sqrt(s0sq)
            delta_rec = basis_rand @ delta_basis_rec
            x_hat_rec = x + (delta_rec[:M] + 1j*delta_rec[M:])
            theta_hat_rec = estimate_theta(x_hat_rec)
            mse_rec += np.rad2deg(theta_hat_rec - theta0)**2
            
            # Anti arm
            vars_anti = np.ones(2*M) * s0sq * kappa**(-1/(2*M-1))
            vars_anti[0] = s0sq * kappa
            delta_basis_anti = z * np.sqrt(vars_anti)
            delta_anti = basis_rand @ delta_basis_anti
            x_hat_anti = x + (delta_anti[:M] + 1j*delta_anti[M:])
            theta_hat_anti = estimate_theta(x_hat_anti)
            mse_anti += np.rad2deg(theta_hat_anti - theta0)**2
        
        mse_inv /= n_trials
        mse_rec /= n_trials
        mse_anti /= n_trials
        
        if prev_inv is not None:
            if not (mse_inv <= mse_rec <= mse_anti):
                shuffled_flip += 1
        prev_inv, prev_rec, prev_anti = mse_inv, mse_rec, mse_anti
    
    return {
        "read_dir": w_hat.tolist(),
        "mse": results["mse"],
        "recon_energy": results["recon_energy"],
        "omission_floor_mult": omission_floor_mult,
        "shuffled_flip": shuffled_flip,
    }