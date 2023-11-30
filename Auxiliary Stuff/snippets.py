

def euro_Csim(r, v, S0, K, T, NSim):
    '''
    r: risk-free rate
    v: volatility
    S0: initial price
    K: strike price
    time: unit of time for simulation
    T: time to maturity (in days)
    NSim: number of simulations
    '''


    # Convert T to years -> 252 trading days per year
    T_y = T / 252

    S = []
    W = np.random.standard_normal(NSim)
    S = S0 * np.exp((r - 0.5 * v**2) * T_y + v * W * np.sqrt(T_y))

    disc_Pay_Call = np.exp(-r * T_y) * np.maximum(S - K, 0)
    mPay_Call = np.mean(disc_Pay_Call)

    return mPay_Call


test = euro_Csim(0.05, 0.2, 100, 100, 150, 10000)
test = [euro_Csim(0.05, 0.2, 90, 100, 150, NSim) for NSim in range(1000,1000001, 1000)]
len(test)
range(1,199)

def black_scholes_closed_form(S0, K, t, r, sigma):
    T  = t / 252
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S0 * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    put_price = K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
    return call_price, put_price

black_scholes_closed_form(90, 100, 150, 0.05, 0.2)

test

d1 = (np.log(90/100) + (0.05 + 0.5 * 0.2**2) * 150/252) / ( 0.2 * np.sqrt(150/252))
d2 = d1 - 0.2 * np.sqrt(150/252)
C = 90 * stats.norm.cdf(d1) - 100 * np.exp(-0.05 * 150/252) * stats.norm.cdf(d2)
C