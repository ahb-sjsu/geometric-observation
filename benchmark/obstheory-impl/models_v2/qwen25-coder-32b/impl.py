import numpy as np

def solve(M, theta0_deg, kappa, s0sq_list, n_trials, seed):
    np.random.seed(seed)
    
    # Convert theta0 to radians
    theta0_rad = np.deg2rad(theta0_deg)
    
    # Define the steering vector a(theta0)
    def steering_vector(theta, M):
        m = np.arange(M)
        return np.exp(1j * np.pi * m * np.sin(theta))
    
    a_theta0 = steering_vector(theta0_rad, M)
    
    # Define the angle estimation function using matched filter
    def estimate_angle(x, M):
        angles = np.linspace(0, np.pi, 1000)  # Fine search over possible angles
        max_corr = 0
        best_theta = 0
        for theta in angles:
            a_theta = steering_vector(theta, M)
            corr = np.abs(np.dot(a_theta.conj(), x))**2
            if corr > max_corr:
                max_corr = corr
                best_theta = theta
        return np.rad2deg(best_theta)
    
    # Compute the informative direction w_hat
    def compute_w_hat(a_theta0):
        a_real = np.real(a_theta0)
        a_imag = np.imag(a_theta0)
        w_hat = np.concatenate((a_real, a_imag))
        w_hat /= np.linalg.norm(w_hat)
        return w_hat
    
    w_hat = compute_w_hat(a_theta0)
    
    # Function to generate delta with given covariance
    def generate_delta(w_hat, s0sq, kappa, M, n_trials, mode):
        dP = 2 * M - 1
        if mode == "invariant":
            variances = np.full(2 * M, s0sq * kappa**(1/dP))
            variances[0] = s0sq / kappa
        elif mode == "recon":
            variances = np.full(2 * M, s0sq)
        elif mode == "anti":
            variances = np.full(2 * M, s0sq * kappa**(-1/dP))
            variances[0] = s0sq * kappa
        elif mode == "omission":
            variances = np.full(2 * M, s0sq * kappa**(1/dP))
            variances[0] = 0.05
        elif mode == "shuffled":
            random_direction = np.random.randn(2 * M)
            random_direction /= np.linalg.norm(random_direction)
            variances = np.full(2 * M, s0sq * kappa**(1/dP))
            variances[0] = s0sq / kappa
        
        cov_matrix = np.diag(variances)
        transform_matrix = np.column_stack((w_hat, np.random.randn(2 * M, dP)))
        transform_matrix, _ = np.linalg.qr(transform_matrix)
        cov_matrix_transformed = transform_matrix @ cov_matrix @ transform_matrix.T
        
        # Ensure the covariance matrix is positive semi-definite
        cov_matrix_transformed = (cov_matrix_transformed + cov_matrix_transformed.T) / 2
        eig_vals, eig_vecs = np.linalg.eigh(cov_matrix_transformed)
        eig_vals = np.maximum(eig_vals, 0)  # Make sure eigenvalues are non-negative
        cov_matrix_transformed = eig_vecs @ np.diag(eig_vals) @ eig_vecs.T
        
        # Generate deltas
        L = np.linalg.cholesky(cov_matrix_transformed)
        deltas = L @ np.random.randn(2 * M, n_trials)
        return deltas.T
    
    # Initialize results
    mse_results = {"invariant": [], "recon": [], "anti": [], "omission": []}
    recon_energy_results = {"invariant": [], "recon": [], "anti": [], "omission": []}
    shuffled_flip = 0
    
    # Source amplitude s with |s| = 1
    s = np.exp(1j * np.random.rand())
    
    # Generate snapshots and perform trials
    for s0sq in s0sq_list:
        x = a_theta0 * s
        
        for mode in ["invariant", "recon", "anti", "omission"]:
            deltas = generate_delta(w_hat, s0sq, kappa, M, n_trials, mode)
            mse = 0
            recon_energy = 0
            
            for delta in deltas:
                delta_contiguous = np.ascontiguousarray(delta)
                x_hat = x + delta_contiguous.view(complex)
                theta_hat = estimate_angle(x_hat, M)
                mse += (theta_hat - theta0_deg)**2
                recon_energy += np.sum(delta**2)
            
            mse_results[mode].append(mse / n_trials)
            recon_energy_results[mode].append(recon_energy / n_trials)
        
        # Shuffled control
        deltas_shuffled = generate_delta(w_hat, s0sq, kappa, M, n_trials, "shuffled")
        mse_shuffled = 0
        
        for delta in deltas_shuffled:
            delta_contiguous = np.ascontiguousarray(delta)
            x_hat = x + delta_contiguous.view(complex)
            theta_hat = estimate_angle(x_hat, M)
            mse_shuffled += (theta_hat - theta0_deg)**2
        
        mse_shuffled /= n_trials
        
        if not (mse_results["invariant"][-1] <= mse_shuffled <= mse_results["anti"][-1]):
            shuffled_flip += 1
    
    # Calculate omission floor multiplier
    omission_mse_max_rate = mse_results["omission"][-1]
    invariant_mse_max_rate = mse_results["invariant"][-1]
    omission_floor_mult = omission_mse_max_rate / invariant_mse_max_rate
    
    return {
        "read_dir": w_hat.tolist(),
        "mse": {"invariant": mse_results["invariant"], "recon": mse_results["recon"], "anti": mse_results["anti"]},
        "recon_energy": {"invariant": recon_energy_results["invariant"], "recon": recon_energy_results["recon"], "anti": recon_energy_results["anti"]},
        "omission_floor_mult": omission_floor_mult,
        "shuffled_flip": shuffled_flip,
    }