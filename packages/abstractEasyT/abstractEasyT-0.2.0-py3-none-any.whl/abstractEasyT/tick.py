from abc import ABC
from abc import abstractmethod


class Tick(ABC):

    @abstractmethod
    def __init__(self, symbol: str):

        self._symbol = symbol

        self.time = None
        self.bid = None
        self.ask = None
        self.last = None
        self.volume = None

    @abstractmethod
    def get_new_tick(self):
        ...
