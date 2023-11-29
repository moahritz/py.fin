
from datetime import datetime
import bisect

class Order(object):
    number = 0

    def __init__(self,limit_price, timestamp = None):
        self.limit_price = limit_price
        self.timestamp = timestamp if timestamp is not None else datetime.now()
        self.ID = Order.number + 1
        Order.number += 1
        #print('Order (ID: %s) created' %(self.ID))
    
    def __str__(self):
        return " Limit Price: %s, Side: %s, Order ID: %s, Timestamp: %s" %(self.limit_price, self.side, self.ID, self.timestamp)

    def __del__(self):
        #print('Order (ID: %s) deleted' %(self.ID))
        pass

class Ask(Order):

        def __init__(self, limit_price, size = 1, side = 'sell', timestamp = None):
            timestamp = timestamp if timestamp is not None else datetime.now()

            Order.__init__(self, limit_price, timestamp)
            self.limit_price = limit_price
            self.size = size
            self.side = side


class Bid(Order):

        def __init__(self, limit_price, size = 1, side = 'buy', timestamp = None):
            timestamp = timestamp if timestamp is not None else datetime.now()

            Order.__init__(self, limit_price, timestamp)
            self.limit_price = limit_price
            self.size = size
            self.side = side


class OrderBook(object):
    def __init__(self, tick_size):
        self.tick_size = tick_size
        self.asks = []
        self.bids = []

        self.price_changes = []
        self.total_volume = 0
        self.spreads = []       #list of all spreads from Trades in OrderBook To calculate avg. spread
        self.hist_spreads = []  #list of the historical average spreads
        self.hist_std = []
        self.trade_prices = []


    def add_order(self, order):
        timestamp = datetime.now()   #when do we ever need this?
        order_key = (order.limit_price, order.timestamp)

        if order.side == 'sell':

            pos = bisect.bisect_right([(ask.limit_price, ask.timestamp) for ask in self.asks], order_key)
            self.asks.insert(pos, order)

            if not self.bids or order.limit_price <= self.get_best_bid():
                self.match_order(order, self.bids)
  
        elif order.side == 'buy':

            pos = bisect.bisect_left([(bid.limit_price, bid.timestamp) for bid in self.bids], order_key)
            self.bids.insert(pos, order)

            if not self.asks or order.limit_price >= self.get_best_ask():
                self.match_order(order, self.asks)

    def is_match(self, new_order, existing_order):
        if new_order.side == 'sell' and existing_order.side == 'buy':
            return new_order.limit_price <= existing_order.limit_price
        
        elif new_order.side == 'buy' and existing_order.side == 'sell':
            return new_order.limit_price >= existing_order.limit_price
        else:
            return False

    def match_order(self, new_order, orders):
        for index, order in enumerate(orders):
            if self.is_match(new_order, order):

                bid_price = new_order.limit_price if new_order.side == 'buy' else order.limit_price
                ask_price = new_order.limit_price if new_order.side == 'sell' else order.limit_price

                trade = Trade(new_order.ID if new_order.side == 'buy' else order.ID, order.ID if new_order.side =='buy' else new_order.ID, bid_price, ask_price, order.limit_price, 1)
                #print("Trade executed: ", trade)

                self.update_trade_metrics(trade)

                orders.pop(index)

                if new_order.side == 'sell':
                    self.asks = [ask for ask in self.asks if ask.ID != new_order.ID]
                else:
                    self.bids = [bid for bid in self.bids if bid.ID != new_order.ID]

                break
    
    def update_trade_metrics(self, trade):
        self.total_volume += trade.size
        self.spreads.append(trade.bid_price - trade.ask_price)

        average_spread = self.get_average_spread()
        self.hist_spreads.append(average_spread)

        if self.trade_prices:
            percentage_change = (trade.price / self.trade_prices[-1]) - 1
            self.price_changes.append(percentage_change)

        std_price_change = self.get_std_dp()
        self.hist_std.append(std_price_change)

        self.trade_prices.append(trade.price)
    
    def get_average_spread(self):
        if not self.spreads:
            return 0
        return sum(self.spreads) / len(self.spreads)
    
    def get_std_dp(self):
        if len(self.price_changes) < 2:
            return 0
        return np.std(self.price_changes)
    

    def get_best_ask(self):
        if not self.asks:
            return None
            
        best_ask = min(self.asks, key = lambda x: x.limit_price)
        return best_ask.limit_price

    def get_best_bid(self):
        if not self.bids:
            return None

        best_bid = max(self.bids, key = lambda x: x.limit_price)
        return best_bid.limit_price     

        
    def display(self):
        print("Total number of orders: %s" % Order.number)
        print("Max bid: %s" % self.get_best_bid())
        print("Min ask: %s" % self.get_best_ask())
        print("Bids: ")
        for bid in self.bids:
            print(bid)
        print("Asks: ")
        for ask in self.asks:
            print(ask)
        

class Trade(object):
    number_of_trades = 0

    def __init__(self, buy_order_id, sell_order_id, bid_price, ask_price, price, size):
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.bid_price = bid_price
        self.ask_price = ask_price
        self.price = price
        self.size = size
        Trade.number_of_trades += 1

    def __str__(self):
        return "(%s) : Buy Order ID: %s, Sell Order ID: %s, Price: %s/%s -> %s, Size: %s" % (Trade.number_of_trades, self.buy_order_id, self.sell_order_id, self.bid_price, self.ask_price, self.price, self.size)
    


def mk_order(fv, pv, k, exchange1, exchange2):
    '''individual orders based on params:
    - fv: fair value
    - pv: private value
    - k: profit constant
    - exchange1: the first exchange order book
    - exchange2: the second exchange order book
    '''

    limit_price = ((fv + pv - k) / exchange1.tick_size)//1 * exchange1.tick_size if pv > 0 else ((fv + pv + k) / exchange2.tick_size)//1 * exchange2.tick_size
    order_side = 'buy' if pv > 0 else 'sell'
    order = Bid(limit_price) if order_side == 'buy' else Ask(limit_price)

    chosen_exchange = None

    if order_side == 'sell':
        best_bid_e1 = exchange1.get_best_bid()
        best_bid_e2 = exchange2.get_best_bid()
        if best_bid_e1 is not None and best_bid_e2 is not None:
            chosen_exchange = exchange1 if best_bid_e1 > best_bid_e2 else exchange2
        elif best_bid_e1 is not None and limit_price <= best_bid_e1:
            chosen_exchange = exchange1
        elif best_bid_e2 is not None and limit_price <= best_bid_e2:
            chosen_exchange = exchange2
    else:  #BUY
        best_ask_e1 = exchange1.get_best_ask()
        best_ask_e2 = exchange2.get_best_ask()
        if best_ask_e1 is not None and best_ask_e2 is not None:
            chosen_exchange = exchange1 if best_ask_e1 < best_ask_e2 else exchange2
        elif best_ask_e1 is not None and limit_price >= best_ask_e1:
            chosen_exchange = exchange1
        elif best_ask_e2 is not None and limit_price >= best_ask_e2:
            chosen_exchange = exchange2

    if chosen_exchange is None:
        chosen_exchange = rng.choice([exchange1, exchange2])

    chosen_exchange.add_order(order)

    return order, chosen_exchange



#Set up for simulations
tick = [0.01, 0.1, 1]
Q = [0,0.001, 0.01, 0.1]
K = [0.1, 1]
fair_value = 100

import numpy as np
rng = np.random.default_rng(1234)

PrV0 = rng.standard_normal(100)
PrV1 = 0.1 * PrV0
PrV = [PrV0, PrV1]

B = rng.uniform(0, 1, 100)
C = rng.choice([-1,1], 100)







### Different parameter choices

simulation_results = []

for A in PrV:
    for k in K:
        for q in Q:
        
            exchange1 = OrderBook(tick[0])
            exchange2 = OrderBook(tick[1])
            fair_value = 100

            for pv, prchange, dirchange in zip(A, B, C):
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
                'sigma_price_change2': exchange2.get_std_dp(),
                'PV': A
            })

simulation_results

import pandas as pd

# Convert the simulation results to a pandas DataFrame
df = pd.DataFrame(simulation_results)

# Save the DataFrame to a CSV file
csv_file_path = 'data/simulation_results.csv' #what's the correct path here?


df.to_csv(csv_file_path, index=False)

# Display the path to the CSV file so it can be downloaded or accessed
csv_file_path

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'df' is the DataFrame containing the simulation results
sns.lineplot(data=df, x='k', y='avg_spread1', hue='q', marker='o')
plt.title('Average Bid-Ask Spread for Each k Value')
plt.xlabel('k Value')
plt.ylabel('Average Bid-Ask Spread')
plt.legend(title='q Value')
plt.show()

head(df)
