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

    return mPay_Call,S



def DO_Csim(S0, K, D, dt, r, v, B, NSim):
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
            if S_euler[j][i - 1] > B:
                S_euler[j][i] = S_euler[j][i - 1] + r * S_euler[j][i - 1] * dt + v * S_euler[j][i - 1] * dW[j][i - 1]
            else:
                S_euler[j][i] = 0
        disc_payoff[j] = np.exp(-r * D) * np.max((S_euler[j][-1] - K, 0))
    
    SimPay = np.mean(disc_payoff)

    return SimPay


    # Parameters
S0 = 100 # Initial stock price
K = 100  # Strike prices
D_values = 84  # days
dt = 1/252  # Daily steps
r = 0.05  # Risk-free rate
v = 0.2 # Volatility
B_values = np.linspace(70, 100, 6)
NSim = 1000  # Number of simulations





def barrier_Csim(S0, K, T, r, v, B, NSim):
    '''
    S0: initial price
    K: strike price
    T: time to maturity (in days)
    r: risk-free rate
    v: volatility
    B: barrier price
    NSim: number of simulations
    '''
    T_y = T / 252

    W = np.random.standard_normal(NSim)
    S = S0 * np.exp((r - 0.5 * v**2) * T_y + v * np.sqrt(T_y) * W)

    # Down-and-Out option

    for i in range(NSim):
        path = S0 * np.exp((r - 0.5 * v**2) * np.linspace(0, T_y, T) + v * np.sqrt(T_y/T) * np.cumsum(np.random.standard_normal(T)))
        if np.min(path) <= B:    # The option becomes worthless if the stock price hits or falls below the barrier at any point
            S[i] = 0

    disc_Pay_Call = np.exp(-r * T_y) * np.maximum(S - K, 0)
    mPay_Call = np.mean(disc_Pay_Call)

    return mPay_Call

# Parameters
S0 = 100  # Initial stock price
K = 100  # Strike price
T = 252  # Time to maturity (in days)
r = 0.05  # Risk-free rate
v = 0.2  # Volatility
NSim = 10000  # Number of simulations
B_values = np.linspace(70, 99, 30)  # Barrier values

# Calculating option prices
euro_prices = [euro_Csim(S0, K, T, r, v, NSim) for _ in B_values]
barrier_prices = [barrier_Csim(S0, K, T, r, v, B, NSim) for B in B_values]
#price_differences = np.array(euro_prices) - np.array(barrier_prices)

# Plotting
plt.figure(figsize=(12, 8))
plt.plot(B_values, euro_prices, label='European Option Prices')
plt.plot(B_values, barrier_prices, label='Barrier Option Prices')
#plt.plot(B_values, price_differences, label='Price Difference (European - Barrier)')
plt.xlabel('Barrier Value')
plt.ylabel('Option Price')
plt.title('Comparison of European and Barrier Option Prices')
plt.legend()
plt.grid(True)
plt.show()

