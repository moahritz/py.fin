
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
            order_book.add_order(self)

class Bid(Order):

        def __init__(self, limit_price, size = 1, side = 'buy', timestamp = None):
            timestamp = timestamp if timestamp is not None else datetime.now()

            Order.__init__(self, limit_price, timestamp)
            self.limit_price = limit_price
            self.size = size
            self.side = side
            order_book.add_order(self)

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


    def match_order(self, new_order, orders):

        sorted_orders  =sorted(orders, key = lambda x: (x[0].limit_price, x[1]))

        for order, _ in sorted_orders: #underscore is: timestamp unpacked but ignored, because not used here
            if new_order.side == 'sell': 
                
                best_bid_price = self.get_best_bid()
                if best_bid_price is not None and order.limit_price >= new_order.limit_price:
                    trade_price = min(best_bid_price, new_order.limit_price)
                    trade_size = new_order.size
                    trade = Trade(new_order.ID, order.ID, trade_price, trade_size)
                    print("Trade %s" % trade)
                    orders.remove(order)
                    del new_order
                    break
            elif new_order.side == 'buy':
                
                best_ask_price = self.get_best_ask()
                if best_ask_price is not None and order.limit_price <= new_order.limit_price:
                    trade_price = min(self.min_ask, new_order.limit_price)
                    trade_size = new_order.size
                    trade = Trade(new_order.ID, order.ID, trade_price, trade_size)
                    print("Trade %s" % trade)
                    orders.remove(order)
                    del new_order
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
    





order1 = Ask(103.5)
print(order1)