from iterative_base import IterativeBase

class IterativeBacktest(IterativeBase):

    def go_long(self, bar, units=None, amount=None):
        if self.position == -1:
            self.buy_instrument(bar, units=-self.units) # close current short position
        if units:
            self.buy_instrument(bar, units=units)
        elif amount:
            if amount == "all":
                amount = self.current_balance
            self.buy_instrument(bar, amount=amount) # go long

    def go_short(self, bar, units=None, amount=None):
        if self.position == 1:
            self.sell_instrument(bar, units=self.units) # close current long position
        if units:
            self.sell_instrument(bar, units=units)
        elif amount:
            if amount == "all":
                amount = self.current_balance
            self.sell_instrument(bar, amount=amount) # go short

    def test_sma_strategy(self, sma_S, sma_L):
        
        # print a statement
        stm = "Testing SMA strategy | {} | SMA_S: {} | SMA_L: {}".format(self.ticker, sma_S, sma_L)
        print(65*"-")
        print(stm)
        print(65*"-")

        # reset everything
        self.position = 0 # initial neutral position
        self.get_data() # reset dataset
        self.current_balance = self.initial_balance # reset initial balance
        self.trades = 0 # reset trades

        # data features
        self.data["sma_S"] = self.data.price.rolling(window=sma_S).mean()
        self.data["sma_L"] = self.data.price.rolling(window=sma_L).mean()
        self.data.dropna(inplace=True)

        # strategy
        for bar in range(len(self.data)-1):
            if self.data["sma_S"].iloc[bar] > self.data["sma_L"].iloc[bar]:
                if self.position in [0, -1]:
                    self.go_long(bar, amount="all")
                    self.position = 1
            if self.data["sma_S"].iloc[bar] < self.data["sma_L"].iloc[bar]:
                if self.position in [0, 1]:
                    self.go_short(bar, amount="all")
                    self.position = -1
        self.close_positions(bar+1)