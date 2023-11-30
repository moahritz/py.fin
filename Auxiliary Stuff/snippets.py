import numpy as np

def mean_monte_carlo_simulation(S0, sigma, T, dt, r, n_simulations):
    """
    Performs a Monte Carlo simulation to estimate the mean stock price path using the Euler discretization method.

    Parameters:
    S0 (float): Initial stock price.
    sigma (float): Volatility.
    T (float): Time horizon in years.
    dt (float): Time step.
    r (float): Risk-free interest rate.
    n_simulations (int): Number of simulated paths.

    Returns:
    numpy.ndarray: Mean stock price path from all simulations.
    numpy.ndarray: Individual stock price path for comparison.
    """
    nsteps = int(T / dt)  # Number of steps
    all_paths = np.zeros((n_simulations, nsteps))  # Array to store all paths

    for sim in range(n_simulations):
        dW = np.sqrt(dt) * np.random.normal(size=nsteps)  # Increments of the Wiener process
        S_euler = np.zeros(nsteps)
        S_euler[0] = S0

        # Euler approximation for each path
        for i in range(1, nsteps):
            S_euler[i] = S_euler[i - 1] + r * S_euler[i - 1] * dt + sigma * S_euler[i - 1] * dW[i - 1]

        all_paths[sim, :] = S_euler

    # Calculating the mean path
    mean_path = np.mean(all_paths, axis=0)

    return mean_path, all_paths




dt = 1 / 252  # Time step
T = 1  # Time horizon
S0 = 100  # Initial stock price


v = 0.2  # Volatility
r = 0.05  # Risk-free interest rate

W_T = np.random.standard_normal(int(T/dt))
S_T = S0 * np.exp((r - 0.5 * v ** 2) * T + v * np.sqrt(T) * W_T)
mcA = np.exp(-r * t) * np.max(np.mean(S_T) - K, 0)