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

class Bid(Order):

        def __init__(self, limit_price, size = 1, side = 'buy'):
            Order.__init__(self, limit_price)
            self.limit_price = limit_price
            self.size = size
            self.side = side



order1 = Ask(100.5)
order2 = Ask(103)
print(order2)


order3 = Bid(102.5)
order4 = Bid(101)
print(order3)

Order.number

print(order1)