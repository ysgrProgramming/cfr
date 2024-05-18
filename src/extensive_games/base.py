from abc import ABC, abstractmethod
from typing import Generator, Iterable
import numpy as np
from dataclasses import dataclass

@dataclass
class ExtensiveGame(ABC):
    init_state: np.ndarray[int]
    range_of_elements: tuple[int, int]

    @property
    def shape(self):
        return self.init_state.shape

    @abstractmethod
    def find_next_states(self, state: np.ndarray[int]) -> Generator[np.ndarray[int], None, None]:
        pass
    
    @abstractmethod
    def find_mirror_states(self, state: np.ndarray[int]) -> Generator[np.ndarray[int], None, None]:
        yield state
    
    @abstractmethod
    def evaluate_state(self, state: np.ndarray[int]) -> int | None:
        return None