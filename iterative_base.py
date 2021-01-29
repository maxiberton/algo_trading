import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn")


class IterativeBase():

    def __init__(self, ticker, start, end, amount, use_spread=True):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.initial_balance = amount
        self.current_balance = amount
        self.units = 0
        self.trades = 0
        self.position = 0
        self.use_spread = use_spread
        self.get_data()

    def get_data(self):
        raw = pd.read_csv("/Users/maxibertonalbornoz/Documents/Python/Udemy/Algorithmic Trading A-Z with Python and ML/Part3_Materials/detailed.csv", parse_dates=["time"], index_col="time")
        raw = raw.loc[self.start:self.end]
        raw["returns"] = np.log(raw.price.div(raw.price.shift(periods=1)))
        
        self.data = raw

# Utilities
    def plot_data(self, cols=None):
        if cols is None:
            cols = "price"
        self.data[cols].plot(figsize=(15,8), title=self.ticker)

    def get_values(self, bar):
        date = str(self.data.index[bar].date())
        price = round(self.data.price.iloc[bar],5)
        spread = round(self.data.spread.iloc[bar],5)
        return date, price, spread

# Check status part
    def print_current_balance(self, bar):
        date, price, spread = self.get_values(bar)
        print("{} | Current Balance: {}".format(date, round(self.current_balance, 2)))

    def print_current_position_value(self, bar):
        date, price, spread = self.get_values(bar)
        cpv = self.units * price
        print("{} | Current Position Value: {}".format(date, round(cpv,2)))

    def print_current_nav(self, bar):
        date, price, spread = self.get_values(bar)
        nav = self.current_balance + self.units * price
        print("{} | Net Asset Value: {}".format(date, round(nav,2)))

# Buy and sell parts
    def buy_instrument(self, bar, units=None, amount=None):
        date, price, spread = self.get_values(bar)
        if self.use_spread == True:
            price += spread/2 # ask price
        if amount is not None:
            units = int(amount/price)
        self.current_balance -= units * price
        self.units += units
        self.trades += 1
        print("{} | Buying {} units for {}".format(date, units, round(price,5)))

    def sell_instrument(self, bar, units=None, amount=None):
        date, price, spread = self.get_values(bar)
        if self.use_spread == True:
            price -= spread/2 # bid price
        if amount is not None:
            units = int(amount/price)
        self.current_balance += units * price
        self.units -= units
        self.trades += 1
        print("{} | Selling {} units for {}".format(date, units, round(price,5)))

    def close_positions(self, bar):
        date, price, spread = self.get_values(bar)
        print(60*"-")
        print(" +++ CLOSING ALL POSITIONS +++ ")
        self.current_balance += self.units * price
        self.current_balance -= (abs(self.units)*spread/2*self.use_spread)
        self.units = 0
        self.trades += 1
        print("Closing position of {} units for {}".format(self.units, price))
        self.print_current_balance(bar)
        perf = (self.current_balance - self.initial_balance) / self.initial_balance * 100
        print("Performance in %: {}".format(perf))
        print("Number of trades executed: {}".format(self.trades))
        print(60*"-")