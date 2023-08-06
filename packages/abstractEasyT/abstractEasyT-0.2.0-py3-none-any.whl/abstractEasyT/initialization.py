from abc import ABC
from abc import abstractmethod


class Initialize(ABC):

    @abstractmethod
    def __int__(self):
        """

        :return:
        """

        self.symbol_initialized = []

    @abstractmethod
    def initialize_platform(self):
        ...

    @abstractmethod
    def initialize_symbol(self, *symbols: str):
        ...

