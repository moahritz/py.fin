class OrderBook(object):
    def __init__(self):
         self.asks = []
         self.bids = []
         #self.tick = 0.1
    def add_order(self, order):
        if order.side == 'sell':
            self.asks.append(order)
        elif order.side == 'buy':
            self.bids.append(order)
        # You might want to sort the orders after adding them
        # LimitOrderBook.asks.sort(key=lambda x: x.limit_price)
        # LimitOrderBook.bids.sort(key=lambda x: x.limit_price, reverse=True)

    def display(self):
         print("Bids: ")
         for bid in self.bids:
           print(bid)
         print("Asks: ")
         for ask in self.asks:
              print(ask)
        
order_book = OrderBook()







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
    def __del__(self):
         Order.number -= 1
         print("Order (ID: %s) deleted" %(self.ID))    

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
order2 = Ask(103)
print(order2)


order3 = Bid(102.5)
order4 = Bid(101)
print(order3)

Order.number

print(order1)

order5 = Ask(34)
print(order5)
Order.number
del order5
Order.number
del order3
Order.number
print(order4)


ASKS = [order1, order2, order5]
ASKS.sort(key=lambda x: x.limit_price)
ASKS[0].limit_price

BIDS = [order3, order4]
BIDS.sort(key=lambda x: x.limit_price, reverse=True)
BIDS[0].limit_price


######################### NEW STUFF ############################


order_book.display()