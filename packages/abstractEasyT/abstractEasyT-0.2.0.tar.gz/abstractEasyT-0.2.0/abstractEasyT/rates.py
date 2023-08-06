from abc import ABC
from abc import abstractmethod

from abstractEasyT.timeframe import TimeFrame


class Rates(ABC):

    @abstractmethod
    def __init__(self,
                 symbol: str,
                 timeframe: TimeFrame,
                 count):

        self._timeframe = timeframe
        self._symbol = symbol.upper()
        self._count = count

        self.time = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.tick_volume = None

    @abstractmethod
    def update_rates(self):
        ...
