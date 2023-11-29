tick = [0.01, 0.1, 1]
q = [0,0.001, 0.01, 0.1]
k = [0.1, 1]
fair_value = 100

rng = np.random.default_rng(1234)

A = rng.standard_normal(100000)
A1 = 0.1 * A
B = rng.uniform(0, 1, 100000)
C = rng.choice([-1,1], 100000)

simulation_results = []

for q in q:
    for k in k:
        exchange1 = OrderBook(tick[0])
        exchange2 = OrderBook(tick[1])
        fair_value = 100
        
        for pv, prchange, dirchange in zip(PrV0, B, C):
            if prchange < q:
                fair_value += dirchange
            else:
                fair_value += dirchange * 0
            order = mk_order(fair_value, pv, k, exchange1, exchange2)

        total_vol = exchange1.total_volume + exchange2.total_volume

        simulation_results.append({
            'k': k,
            'q': q,
            'tick1': exchange1.tick_size,
            'tick2':exchange2.tick_size,
            'avg_spread1': exchange1.get_average_spread(),
            'avg_spread2': exchange2.get_average_spread(),
            'sigma_price_change1': exchange1.get_std_dp(),
            'sigma_price_change2': exchange2.get_std_dp()

        })

simulation_results