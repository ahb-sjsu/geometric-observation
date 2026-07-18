```python
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
    
    # Continuous angle estimator using Newton-Raphson method
    def estimate_angle(x, M):
        def cost_function(theta):
            a = steering_vector(theta, M)
            return -np.abs(a.conj().T @ x) ** 2
        
        def gradient(theta):
            a = steering_vector(theta, M)
            da_dtheta = 1j * np.pi * np.cos(theta) * np.arange(M) * a
            return 2 * np.real((a.conj().T @ x) * (da_dtheta.conj().T @ x))
        
        theta_hat = theta0_rad  # Initial guess
        tolerance = 1e-6
        max_iterations = 1000
        
        for _ in range(max_iterations):
            grad = gradient(theta_hat)
            if np.abs(grad) < tolerance:
                break
            theta_hat -= grad / (2 * np.abs(a_theta0.conj().T @ x) ** 2 * np.pi * np.cos(theta_hat) * np.sum(np.arange(M) ** 2))
        
        return np.rad2deg(theta_hat)
    
    # Determine the informative direction w_hat
    def compute_w_hat(a_theta0):
        Re_a = np.real(a_theta0)
        Im_a = np.imag(a_theta0)
        w_hat = np.concatenate([Re_a, Im_a])
        w_hat /= np.linalg.norm(w_hat)
        return w_hat
    
    w_hat = compute_w_hat(a_theta0)
    
    # Generate random unit direction for shuffled control
    def random_unit_vector(dimension):
        v = np.random.randn(dimension)
        v /= np.linalg.norm(v)
        return v
    
    # Function to generate delta with given covariance
    def generate_delta(w_hat, s0sq, kappa, dimension, mode):
        if mode == "invariant":
            cov = np.diag([s0sq / kappa] + [s0sq * kappa**(1/(dimension-1))] * (dimension-1))
        elif mode == "recon":
            cov = np.eye(dimension) * s0sq
        elif mode == "anti":
            cov = np.diag([s0sq * kappa] + [s0sq * kappa**(-1/(dimension-1))] * (dimension-1))
        elif mode == "omission":
            cov = np.diag([0.05] + [s0sq * kappa**(1/(dimension-1))] * (dimension-1))
        elif mode == "shuffled":
            random_direction = random_unit_vector(dimension)
            cov = np.diag([s0sq / kappa] + [s0sq * kappa**(1/(dimension-1))] * (dimension-1))
            P = np.column_stack((random_direction, np.eye(dimension)[:, 1:]))
            cov = P @ cov @ P.T
        else:
            raise ValueError("Unknown mode")
        
        L = np.linalg.cholesky(cov)
        delta = L @ np.random.randn(dimension)
        return delta
    
    # Function to compute reconstruction energy
    def compute_recon_energy(delta, w_hat):
        return np.abs(w_hat.T @ delta) ** 2
    
    # Initialize results
    mse_results = {"invariant": [], "recon": [], "anti": [], "omission": []}
    recon_energy_results = {"invariant": [], "recon": [], "anti": [], "omission": []}
    shuffled_flip = 0
    
    dimension = 2 * M
    
    # Sweep over s0sq_list
    for s0sq in s0sq_list:
        mse_invariant = []
        mse_recon = []
        mse_anti = []
        mse_omission = []
        recon_energy_invariant = []
        recon_energy_recon = []
        recon_energy_anti = []
        recon_energy_omission = []
        
        for _ in range(n_trials):
            # Generate the true snapshot x
            s = np.exp(1j * np.random.rand())  # Random phase for source amplitude
            delta_invariant = generate_delta(w_hat, s0sq, kappa, dimension, "invariant")
            delta_recon = generate_delta(w_hat, s0sq, kappa, dimension, "recon")
            delta_anti = generate_delta(w_hat, s0sq, kappa, dimension, "anti")
            delta_omission = generate_delta(w_hat, s0sq, kappa, dimension, "omission")
            
            x = a_theta0 * s
            
            # Form x_hat and estimate theta_hat
            x_hat_invariant = x + delta_invariant.reshape(M) * (1 + 1j)
            x_hat_recon = x + delta_recon.reshape(M) * (1 + 1j)
            x_hat_anti = x + delta_anti.reshape(M) * (1 + 1j)
            x_hat_omission = x + delta_omission.reshape(M) * (1 + 1j)
            
            theta_hat_invariant = estimate_angle(x_hat_invariant, M)
            theta_hat_recon = estimate_angle(x_hat_recon, M)
            theta_hat_anti = estimate_angle(x_hat_anti, M)
            theta_hat_omission = estimate_angle(x_hat_omission, M)
            
            # Record squared angle errors
            mse_invariant.append((theta_hat_invariant - theta0_deg) ** 2)
            mse_recon.append((theta_hat_recon - theta0_deg) ** 2)
            mse_anti.append((theta_hat_anti - theta0_deg) ** 2)
            mse_omission.append((theta_hat_omission - theta0_deg) ** 2)
            
            # Record reconstruction energies
            recon_energy_invariant.append(compute_recon_energy(delta_invariant, w_hat))
            recon_energy_recon.append(compute_recon_energy(delta_recon, w_hat))
            recon_energy_anti.append(compute_recon_energy(delta_anti, w_hat))
            recon_energy_omission.append(compute_recon_energy(delta_omission, w_hat))
        
        # Average results over trials
        mse_results["invariant"].append(np.mean(mse_invariant))
        mse_results["recon"].append(np.mean(mse_recon))
        mse_results["anti"].append(np.mean(mse_anti))
        mse_results["omission"].append(np.mean(mse_omission))
        
        recon_energy_results["invariant"].append(np.mean(recon_energy_invariant))
        recon_energy_results["recon"].append(np.mean(recon_energy_recon))
        recon_energy_results["anti"].append(np.mean(recon_energy_anti))
        recon_energy_results["omission"].append(np.mean(recon_energy_omission))
    
    # Compute omission floor multiplier
    omission_floor_mult = mse_results["omission"][-1] / mse_results["invariant"][-1]
    
    # Shuffled control
    for s0sq in s0sq_list:
        mse_shuffled = []
        recon_energy_shuffled = []
        
        for _ in range(n_trials):
            delta_shuffled = generate_delta(w_hat, s0sq, kappa, dimension, "shuffled")
            x = a_theta0 * s
            x_hat_shuffled = x + delta_shuffled.reshape(M) * (1 + 1j)
            theta_hat_shuffled = estimate_angle(x_hat_shuffled, M)
            mse_shuffled.append((theta_hat_shuffled - theta0_deg) ** 2)
            recon_energy_shuffled.append(compute_recon_energy(delta_shuffled, w_hat))
        
        # Check the flip condition
        if not (np.mean(mse_results["invariant"]) <= np.mean(mse_shuffled) <= np.mean(mse_results["anti"])):
            shuffled_flip += 1
    
    return {
        "read_dir": w_hat,
        "mse": {"invariant": mse_results["invariant"], "recon": mse_results["recon"], "anti": mse_results["anti"]},
        "recon_energy": {"invariant": recon_energy_results["invariant"], "recon": recon_energy_results["recon"], "anti": recon_energy_results["anti"]},
        "omission_floor_mult": omission_floor_mult,
        "shuffled_flip": shuffled_flip,
    }
```