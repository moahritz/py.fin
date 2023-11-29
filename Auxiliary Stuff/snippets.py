

# Example usage with the parameters from the provided R script
S0 = 100
sigma = 0.2
T = 1
dt = 1/252
r = 0.05
n = 100000

def mc_euler(S0, sigma, T, dt, r, n_simulations):
    """
    Performs a Monte Carlo simulation to estimate the mean stock price at the final time step using the Euler method.

    Parameters:
    S0 (float): Initial stock price.
    mu (float): Drift coefficient.
    sigma (float): Volatility.
    T (float): Time horizon in years.
    dt (float): Time step.
    r (float): Risk-free interest rate.
    n_simulations (int): Number of simulated paths.

    Returns:
    float: Mean stock price at the final time step from all simulations.
    """
    nsteps = int(T / dt)  # Number of steps
    final_prices = np.zeros(n_simulations)  # Array to store the final price of each path

    for sim in range(n_simulations):
        dW = np.sqrt(dt) * np.random.normal(size=nsteps)  # Increments of the Wiener process
        S_euler = np.zeros(nsteps)
        S_euler[0] = S0

        # Euler approximation for each path
        for i in range(1, nsteps):
            S_euler[i] = S_euler[i - 1] + r * S_euler[i - 1] * dt + sigma * S_euler[i - 1] * dW[i - 1]

        final_prices[sim] = S_euler[-1]

    # Calculating the mean of the final prices
    mean_final_price = np.mean(final_prices)

    return mean_final_price

# Testing the updated function with 10 simulations
mean_final_price_test = mc_euler(S0, sigma, T, dt, r, n)
mean_final_price_test

