
import numpy as np
import scipy.stats as stats


def asia_Csim(S0, K, T, dt, r, v, NSim):
    '''
    S0: initial stock price
    K: strike price
    T: Time to maturity 
    dt: time step
    r: risk free rate
    v: volatility
    NSim: number of simulations
    '''
    nsteps = int((D / 252)/ dt)    #daily steps
    S_euler = np.zeros((NSim, nsteps)) 
    dW = np.zeros((NSim, nsteps))
    disc_payoff = np.zeros(NSim)

    for j in range(NSim):
        dW[j] = np.sqrt(dt) * np.random.standard_normal(nsteps)
        S_euler[j][0] = S0

        for i in range(1, nsteps):
            S_euler[j][i] = S_euler[j][i - 1] + r * S_euler[j][i - 1] * dt + v * S_euler[j][i - 1] * dW[j][i - 1]
        disc_payoff[j] = np.exp(-r * D) * np.max((np.mean(S_euler[j]) - K, 0))
    
    SimPay = np.mean(disc_payoff)

    return SimPay


def euro_Csim(S0, K, T, r, v, NSim):
    '''
    S0: initial price
    K: strike price
    T: time to maturity (in days)
    r: risk-free rate
    v: volatility
    NSim: number of simulations
    '''

    # Convert T to years -> 252 trading days per year
    T_y = T / 252

    S = []
    W = np.random.standard_normal(NSim)
    S = S0 * np.exp((r - 0.5 * v**2) * T_y + v * np.sqrt(T_y) * W)

    disc_Pay_Call = np.exp(-r * T_y) * np.maximum(S - K, 0)
    mPay_Call = np.mean(disc_Pay_Call)

    return mPay_Call

euro_Csim(100, 100, 30, 0.05, 0.2, 10000)
asia_Csim(100, 100, 30, 1/252, 0.05, 0.2, 10000)




import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


# Function to simulate European Call option prices using the same Monte Carlo approach
def euro_Csim(S0, K, D, dt, r, v, NSim):
    T = D * dt
    n = int(T/dt)
    S = np.zeros((n+1, NSim))
    S[0] = S0
    for t in range(1, n+1):
        z = np.random.standard_normal(NSim)
        S[t] = S[t-1] * np.exp((r - 0.5 * (v ** 2)) * dt + v * np.sqrt(dt) * z)
    C = np.exp(-r * T) * np.sum(np.maximum(S[-1] - K, 0)) / NSim
    return C

# Parameters
S0 = 100  # Initial stock price
K_values = np.linspace(80, 120, 10)  # Strike prices
D = 26  # days
dt = 1/252  # Daily steps
r = 0.05  # Risk-free rate
v = 0.2  # Volatility
NSim = 10000  # Number of simulations

# Collecting option prices for different strike prices
asia_prices = []
euro_prices = []

for K in K_values:
    asia_price = asia_Csim(S0, K, D, dt, r, v, NSim)
    euro_price = euro_Csim(S0, K, D, dt, r, v, NSim)
    asia_prices.append(asia_price)
    euro_prices.append(euro_price)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(K_values, asia_prices, label='Asian Call Option', marker='o')
plt.plot(K_values, euro_prices, label='European Call Option', marker='x')
plt.xlabel('Strike Price (K)')
plt.ylabel('Option Price')
plt.title('Comparison of Asian and European Call Option Prices')
plt.legend()
plt.grid(True)
plt.show()

