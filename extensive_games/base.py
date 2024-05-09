from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Generator
from dataclasses import dataclass

@dataclass
class ExtensiveGame(ABC):
    n: int

    @abstractmethod
    def get_actions(self, history: list[int] = []) -> Generator[int, None, None]:
        pass

    @abstractmethod
    def get_active_player(self, history: list[int]) -> int:
        pass

    @abstractmethod
    def get_information_tuple(self, history: list[int]) -> tuple[int]:
        pass

    @abstractmethod
    def get_utility(self, history: list[int]) -> float | None:
        pass