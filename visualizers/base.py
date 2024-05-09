from pydantic import BaseModel
from abc import ABC, abstractmethod
from extensive_games import ExtensiveGame
from strategy import Strategy
from dataclasses import dataclass

@dataclass
class Visualizer(ABC):
    game: ExtensiveGame
    strategy: Strategy | None

    @abstractmethod
    def visualize(self, history):
        pass