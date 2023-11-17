
#1. Order Matching Logic Improvement:
#Modify the match_order function to sort the orders based on price and time before trying to match.
#Add a timestamp attribute to orders to support this.
#2. Price Comparison Logic:
#Implement methods to retrieve the best bid and ask prices from the OrderBook.
#3. Error Handling:
#Instead of using del new_order, we will handle the order size reduction within the match_order function.
#4. Trade Execution Side Effects:
#Adjust the sizes of the orders in the match_order function when a trade occurs.
#5. Encapsulation:
#Add methods for order cancellation and modification.
#6. Data Structures:
#For now, we will keep the list data structure for simplicity. If performance becomes an issue, we could consider using heaps.
#7. Robust Trade Class:
#Include additional attributes such as timestamps and trade IDs in the Trade class.
#8. Testing and Validation:
#Outline a simple testing procedure to validate the behavior of the OrderBook.



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
        self.max_bid =  None  #DELETE LATER
        self.min_ask =  None  #DELETE LATER

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
                trade = Trade(new_order.ID, order.ID, order.limit_price, 1)
                print("Trade executed: ", trade)

                orders.pop(index)

                if new_order.side == 'sell':
                    self.asks = [ask for ask in self.asks if ask.ID != new_order.ID]
                else:
                    self.bids = [bid for bid in self.bids if bid.ID != new_order.ID]

                break

        # Update max_bid and min_ask
        self.max_bid = max([bid.limit_price for bid in self.bids]) if self.bids else None  #DELETE LATER
        self.min_ask = min([ask.limit_price for ask in self.asks]) if self.asks else None  #DELETE LATER

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

    def __init__(self, buy_order_id, sell_order_id, price, size):
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.price = price
        self.size = size
        Trade.number_of_trades += 1

    def __str__(self):
        return "(%s) : Buy Order ID: %s, Sell Order ID: %s, Price: %s, Size: %s" % (Trade.number_of_trades, self.buy_order_id, self.sell_order_id, self.price, self.size)
    


def mk_order(fv, pv, k, exchange1, exchange2):
    '''Create individual orders based on the fair value, the private value, and the constant profit.
    Parameters:
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

exchange1 = OrderBook(tick1)
exchange2 = OrderBook(tick2)

import numpy as np
rng = np.random.default_rng(1234)

A = rng.standard_normal(10000)
A1 = 0.1 * A
B = rng.uniform(0, 1, 10000)
C = rng.choice([-1,1], 10000)

fair_value = 100
k = .1
tick1 = .01
q = 0.01

tick1 = 0.01
tick2 = 0.01




### Different parameter choices

for pv, prchange, dirchange in zip(A, B, C):
    if prchange < q:
        fair_value += dirchange
    else:
        fair_value += dirchange * 0
    order = mk_order(fair_value, pv, k, exchange1, exchange2) 

exchange1.display()