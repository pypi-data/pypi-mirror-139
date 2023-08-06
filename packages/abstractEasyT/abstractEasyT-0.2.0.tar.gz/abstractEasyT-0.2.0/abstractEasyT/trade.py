from abc import ABC
from abc import abstractmethod


class Trade(ABC):

    @abstractmethod
    def __init__(self,
                 symbol: str,
                 lot: float,
                 stop_loss,
                 take_profit
                 ):
        self.symbol = symbol.upper()
        self.lot = lot
        self.stop_loss = stop_loss
        self.take_profit = take_profit

        self._trade_allowed = False

        self.trade_direction = None  # 'buy', 'sell', or None for no position
        self.position_check()

    @abstractmethod
    def open_buy(self):
        ...

    @abstractmethod
    def open_sell(self):
        ...

    @abstractmethod
    def position_open(self, buy: bool, sell: bool):
        if self._trade_allowed and self.trade_direction is None:
            if buy and not sell:
                self.open_buy()
                self.position_check()

            if sell and not buy:
                self.open_sell()
                self.position_check()

    @abstractmethod
    def position_close(self):
        if self.trade_direction == 'buy':
            self.open_sell()
            self.position_check()

        elif self.trade_direction == 'sell':
            self.open_buy()
            self.position_check()

    @abstractmethod
    def position_check(self):
        ...
