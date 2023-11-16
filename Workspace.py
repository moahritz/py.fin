class OrderBook(object):
    def __init__(self, tick_size):
        self.tick_size = tick_size
        self.asks = []
        self.bids = []
        self.max_bid =  None
        self.min_ask =  None

    def add_order(self, order):
        if order.side == 'sell':
            if (self.max_bid is None) or (order.limit_price > self.max_bid):
                if self.min_ask is None or order.limit_price < self.min_ask:
                    self.min_ask = order.limit_price
                    self.asks.append(order)
                else:  
                    self.asks.append(order)
            else:
                self.match_order(order, self.bids)
  
        elif order.side == 'buy':
            if self.min_ask is None:  
                if self.max_bid is None or order.limit_price > self.max_bid:
                    self.max_bid = order.limit_price
                    self.bids.append(order)
                else:
                    self.bids.append(order)
            elif order.limit_price < self.min_ask:
                if self.max_bid is None or order.limit_price > self.max_bid:
                    self.max_bid = order.limit_price
                    self.bids.append(order)
                else:
                    self.bids.append(order)
            else:
               self.match_order(order, self.asks)


    def match_order(self, new_order, orders):
        for order in orders:
            if new_order.side == 'buy' and order.limit_price <= new_order.limit_price:
                trade_price = min(self.min_ask, new_order.limit_price)
                trade_size = new_order.size
                trade = Trade(new_order.ID, order.ID, trade_price, trade_size)
                print("Trade %s" % trade)
                orders.remove(order)
                del new_order
                break
            elif new_order.side == 'sell' and order.limit_price >= new_order.limit_price:
                trade_price = min(self.min_ask, new_order.limit_price)
                trade_size = new_order.size
                trade = Trade(new_order.ID, order.ID, trade_price, trade_size)
                print("Trade %s" % trade)
                orders.remove(order)
                del new_order
                break
        # Update max_bid and min_ask
        self.max_bid = max([bid.limit_price for bid in self.bids]) if self.bids else None
        self.min_ask = min([ask.limit_price for ask in self.asks]) if self.asks else None
        

        
    def display(self):
        print("Total number of orders: %s" % Order.number)
        print("Max bid: %s" % self.max_bid)
        print("Min ask: %s" % self.min_ask)
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
    

class Order(object):
    number = 0

    def __init__(self,limit_price):
        self.limit_price = limit_price
        self.ID = Order.number + 1
        Order.number += 1
        #print('Order (ID: %s) created' %(self.ID))
    
    def __str__(self):
        return " Limit Price: %s, Side: %s, Order ID: %s" %(self.limit_price, self.side, self.ID)

    def __del__(self):
        #print('Order (ID: %s) deleted' %(self.ID))
        pass

class Ask(Order):

        def __init__(self, limit_price, size = 1, side = 'sell'):
            Order.__init__(self, limit_price)
            self.limit_price = limit_price
            self.size = size
            self.side = side
            order_book.add_order(self)

class Bid(Order):

        def __init__(self, limit_price, size = 1, side = 'buy'):
            Order.__init__(self, limit_price)
            self.limit_price = limit_price
            self.size = size
            self.side = side
            order_book.add_order(self)




order_book =OrderBook(0.0001)
order_book.display()
order1 = Ask(100.5)
order_book.display()
order2 = Ask(103)
order_book.display()
order3 = Bid(102.5)
order_book.display()
order4 = Bid(101)
order_book.display()
order5 = Ask(34)
order_book.display()
order6 = Bid(104)
order_book.display()
order7 = Ask(100)
order_book.display()
order8 = Bid(105)
order_book.display()
order9 = Bid(25)
order_book.display()
Trade.number_of_trades



















##### 2. Generating random numbers and simulating order flow
import numpy as np

rng = np.random.default_rng(123)

A = rng.standard_normal(100)
B = rng.uniform(0, 1, 100)
C = rng.choice([-1,1], 100)
D = rng.choice(['EX1', 'EX2'], 100000)

def mk_order(fv, pv, k, Order_Book):
    '''
    Create individual orders based on the fair value, the private value, the constant profit, and the tick size.

    Parameters:
    - fv: fair value
    - pv: private value
    - k: profit constant
    - Order_Book: the order book to which the order will be added, and that holds the tick_size as an argument
    '''

    if pv >= 0:
        #This is a buy order
        limit_price = round((fv + pv - k) /Order_Book.tick_size) * Order_Book.tick_size 
        order = Bid(limit_price)
    else:
        #This is a sell order
        limit_price = round((fv + pv + k) /Order_Book.tick_size) * Order_Book.tick_size
        order = Ask(limit_price)

    return order




###### 3. Starting the Simulations ######
fair_value = 100
k = .1
tick1 = .01
q = 0.3


EX1 = OrderBook(tick1)

order1 = Bid(((100 + A[6] - 0.1)/EX1.tick_size)//1 * EX1.tick_size)
order2 = Ask(((100 + A[6] - 0.1)/EX1.tick_size)//1 * EX1.tick_size)
order3 = Ask(23.34)


order_book.display()
order_book.display()


for pv, prchange, dirchange in zip(A, B, C):
    if prchange < q:
        fair_value += dirchange
    else:
        fair_value += dirchange * 0
    order = mk_order(fair_value, pv, k, EX1) 



for pv, prchange, dirchange in zip(A,B,C):
    if prchange < q:
        fair_value += dirchange
    order = mk_order(fair_value, pv, k, EX1)
    test.append(order)


test =[]
for pv in A:
    limit_price = ((fair_value + pv - k) /EX1.tick_size)//1 * EX1.tick_size
    test.append(limit_price)

test