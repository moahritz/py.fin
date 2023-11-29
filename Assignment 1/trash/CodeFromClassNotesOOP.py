import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt



###################################################
###################################################
###################################################

cor = np.identity(5) \
+ np.diag([0.6,0.6,0.6,0.6], k=1) + np.diag([0.6,0.6,0.6,0.6], k=-1)  + np.diag([0.3,0.3,0.3], k=2) + np.diag([0.3,0.3,0.3], k=-2) \
+ np.diag([-0.3],k=4) + np.diag([-0.3],k=-4)
cor


prices = np.array([100, 101.97, 102.68, 100.92, 100.38, 100.91, 102.76, 105.05, 105.07, 106.37, 107.67, 108.61, 109.57, 110.66, 110.39, 110.26, 109.25, 108.04, 108.62, 108.5, 108.73])

total_return = (prices[-1] - prices[0]) / prices[0]
print("Total arithmetic return over the period: " + str(round(total_return, 4)))

# Choose one week randomly and compute its weekly return
rng = np.random.default_rng()
random_week_start = rng.choice(np.arange(0, 16))  # 16 is chosen to ensure a full week of data
weekly_return = (prices[random_week_start + 5] - prices[random_week_start]) / prices[random_week_start]
print("Weekly return for randomly chosen week starting at day " +str(random_week_start + 1)+ ": " + str(round(weekly_return, 4)))

###################################################
###################################################
###################################################


#The __init__ method is called a constructor. It is used to create a new instance of the class.
#All classes have a function called __init__(), which is always executed when the class is being initiated.

class Stock(object):
    def __init__(self, symbol, price, dividend = 0):
        self.symbol = symbol 
        self.price = price 
        self.dividend = dividend #self.attribute means that attribute is an attribute of the object and not of the class.

apple = Stock(symbol='AAPL',price=987.65) 
microsoft = Stock('MSFT',43.21,1)

apple.symbol
microsoft.symbol

#Apart from the object attributes, there also exist class attributes. Their values are assigned to the whole class rather than to an individual instance. Class attributes are defined outside any methods, usually at the beginning of the code defining the class.

#number as class attribute

class Stock(object):
    number = 0
    def __init__(self, symbol, price, dividend = 0):
        self.symbol = symbol
        self.price = price
        self.dividend = dividend
        Stock.number += 1

apple = Stock('AAPL',987.65, dividend = 35)
microsoft = Stock('MSFT',43.21,1)

Stock.number

## METHODS

#Methods are functions that are defined inside a class. They are used to define the behaviors of an object. it is possible to make attributes accessible only through methods.

class Stock(object):
    number = 0
    tick = 0.01

    def __init__(self, symbol, price, dividend = 0):
        self.symbol = symbol
        self.price = price
        self.dividend = dividend
        Stock.number += 1
    
    def yield_percent(self):
        return self.dividend / self.price * 100
    
    def relative_ticksize(self):
        return Stock.tick / self.price * 10000
    
    def set_dividend(self, dividend):
        self.dividend = dividend

    def get_dividend(self):
        return self.dividend
    

apple = Stock('AAPL',987.65, dividend = 35)
microsoft = Stock('MSFT',43.21,1)

apple.yield_percent()
microsoft.relative_ticksize()

microsoft.set_dividend(30)
microsoft.get_dividend()


## STATIC METHODS

# Static methods apply to the whole class and are not specific to an individual object.

class Stock(object):
    number = 0
    tick = 0.01

    def __init__(self, symbol, price, dividend = 0):
        self.symbol = symbol
        self.price = price
        self.dividend = dividend
        Stock.number += 1

    def get_number():           # static method
        return Stock.number
    
    def yield_percent(self):
        return self.dividend / self.price * 100
    
    def relative_ticksize(self):
        return Stock.tick / self.price * 10000
    
    def set_dividend(self, dividend):
        self.dividend = dividend

    def get_dividend(self):
        return self.dividend

apple = Stock(symbol='AAPL',price=987.65, dividend=35) 
microsoft = Stock('MSFT',43.21, 1)

Stock.get_number()

## INHERITANCE

# Inheritance is a way to form new classes using classes that have already been defined. The newly formed classes are called derived classes, the classes that we derive from are called base classes. Important benefits of inheritance are code reuse and reduction of complexity of a program. The derived classes (descendants) override or extend the functionality of base classes (ancestors).

class FinancialInstrument(object):
    number = 0
    def __init__(self, price):
        self.price = price
        print('instrument created')

    def get_number():
        pass

    def yield_percent(self):
        pass

class Stock(FinancialInstrument):
    tick = 0.01

    def __init__(self, symbol, price, dividend = 0):
        FinancialInstrument.__init__(self, price)
        self.symbol = symbol
        self.price = price
        self.dividend = dividend
        Stock.number += 1

    def get_number():           # static method
        return Stock.number
    
    def yield_percent(self):
        return self.dividend / self.price * 100
    
    def relative_ticksize(self):
        return Stock.tick / self.price * 10000
    
    def set_dividend(self, dividend):
        self.dividend = dividend

    def get_dividend(self):
        return self.dividend
    
class Bond(FinancialInstrument):
    def __init__(self, cusip, price, coupon = 0):
        FinancialInstrument.__init__(self, price) 
        self.cusip = cusip
        self.coupon = coupon
        Bond.number+=1
    def get_number():
        return Bond.number
    def yield_percent(self):
        return self.coupon / self.price *100

apple = Stock('AAPL',987.65, dividend = 35)
microsoft = Stock('MSFT',43.21,1)

Stock.get_number()

bond1 = Bond('US912810EV37', 100.5, 1.5)
bond1.yield_percent()
Bond.get_number()


## SPECIAL METHODS

#The methods prefixed and suffixed by __ are private, i.e., they cannot be directly called from outside the module. We can call them here only because we are operating in the same namespace , i.e., we haven't saved the class in a module that we would have to import to use it.

class Stock(FinancialInstrument):
    tick = 0.01

    def __init__(self, symbol, price, dividend = 0):
        FinancialInstrument.__init__(self, price)
        self.symbol = symbol
        self.dividend = dividend
        Stock.number += 1

    def __str__(self):
        return "Symbol: %s , Price: %s , Dividend: %s " %(self.symbol, self.price, self.dividend)
    def __len__(self):
        return len(self.symbol)
    def __del__(self):
        Stock.number -= 1
        print('%s has been deleted!' %(self.symbol))


apple = Stock('AAPL',987.65, dividend = 35)
microsoft = Stock('MSFT',43.21,1)

print(microsoft)
print(len(microsoft))
del microsoft
Stock.number

apple.__len__()











