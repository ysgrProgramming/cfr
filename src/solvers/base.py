from abc import ABC, abstractmethod
from ..model import Model
from ..strategy import Strategy
from dataclasses import dataclass

@dataclass
class StrategyMaker(ABC):
    parameters: dict = dict()

    @abstractmethod
    def make_strategy(self, model: Model) -> Strategy:
        pass