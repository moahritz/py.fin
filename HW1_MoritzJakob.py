####### 1. Implementing a limit oder market

class OrderBook(object):
    def __init__(self):
        self.asks = []
        self.bids = []
        self.min_bid = None
        self.max_ask = None

    def add_order(self, order):
        if order.side == 'sell':
            if self.min_bid is not None and order.limit_price <= self.min_bid:
                self.match_orders(order, self.bids)
            else:
                self.asks.append(order)
                if self.max_ask is None or order.limit_price > self.max_ask:
                    self.max_ask = order.limit_price
        elif order.side == 'buy':
            if self.max_ask is not None and order.limit_price >= self.max_ask:
                self.match_orders(order, self.asks)
            else:
                self.bids.append(order)
                if self.min_bid is None or order.limit_price < self.min_bid:
                    self.min_bid = order.limit_price

    def match_orders(self, new_order, orders):
        for order in orders:
            if new_order.side == 'buy' and order.limit_price <= new_order.limit_price:
                trade_price = order.limit_price
                trade_size = min(new_order.size, order.size)
                trade = Trade(new_order.ID, order.ID, trade_price, trade_size)
                print("Trade: %s" % trade)
                orders.remove(order)
                new_order.size -= trade_size
                if new_order.size == 0:
                    break
            elif new_order.side == 'sell' and order.limit_price >= new_order.limit_price:
                trade_price = order.limit_price
                trade_size = min(new_order.size, order.size)
                trade = Trade(new_order.ID, order.ID, trade_price, trade_size)
                print("Trade: %s" % trade)
                orders.remove(order)
                new_order.size -= trade_size
                if new_order.size == 0:
                    break
            
        # Update min_bid and max_ask
        self.min_bid = min([bid.limit_price for bid in self.bids]) if self.bids else None
        self.max_ask = max([ask.limit_price for ask in self.asks]) if self.asks else None

    def display(self):
        print("Total number of orders: %s" % Order.number)
        print("Min bid: %s" % self.min_bid)
        print("Max ask: %s" % self.max_ask)
        print("Bids: ")
        for bid in self.bids:
            print(bid)
        print("Asks: ")
        for ask in self.asks:
            print(ask)
        
order_book = OrderBook()

class Trade(object):
    def __init__(self, buy_order_id, sell_order_id, price, size):
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.price = price
        self.size = size

    def __str__(self):
        return "Buy Order ID: %s, Sell Order ID: %s, Price: %s, Size: %s" % (self.buy_order_id, self.sell_order_id, self.price, self.size)





class Order(object):
    number = 0

    def __init__(self,limit_price):
        self.limit_price = limit_price
        self.ID = Order.number + 1
        Order.number += 1
        print('Order (ID: %s) created' %(self.ID))
    
    def __str__(self):
        return " Limit Price: %s, Side: %s, Order ID: %s" %(self.limit_price, self.side, self.ID)

    def get_number(self):
        return self.ID


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





######### TEST AREA ########
order1 = Ask(100.5)
order_book.display()
order2 = Ask(103)
order_book.display()
#print(order2)

order3 = Bid(102.5)

order_book.display()
order4 = Bid(101)
order_book.display()
#print(order3)

Order.number

#print(order1)

order5 = Ask(34)
#print(order5)
order_book.display()
order6 = Bid(104)
order_book.display()
order7 = Ask(100)
order_book.display()
order8 = Bid(105)
order_book.display()
######################### NEW STUFF ############################

##### 2. Generating random numbers and simulating order flow

