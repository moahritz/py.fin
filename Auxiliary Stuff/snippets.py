
import numpy as np
import scipy.stats as stats


def asia_Csim(S0, K, D, dt, r, v, NSim):
    '''
    S0: initial stock price
    K: strike price
    D: Days to maturity (in years)
    dt: time step
    r: risk free rate
    v: volatility
    NSim: number of simulations
    '''
    nsteps = int(((D - 1)/ 252)/ dt)    #daily steps
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



# Black-Scholes for call and put options
def black_scholes_closed_form(S0, K, T, r, v):
    T_y  = T / 252
    d1 = (np.log(S0 / K) + (r + v**2 / 2) * T_y) / (v * np.sqrt(T_y))
    d2 = d1 - v * np.sqrt(T_y)
    call_price = S0 * stats.norm.cdf(d1) - K * np.exp(-r * T_y) * stats.norm.cdf(d2)
    return call_price


asia_Csim(100, 100, 252, 1/252, 0.05, 0.2, 100000)
