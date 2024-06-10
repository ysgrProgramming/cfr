from abc import ABC, abstractmethod
from ..model import Model
from ..strategy import Strategy

class StrategyMaker(ABC):
    @abstractmethod
    def make_strategy(self, model: Model) -> Strategy:
        pass