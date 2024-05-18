import numpy as np
from dataclasses import dataclass

class StateHashConverter:
    def __init__(self, shape: tuple, range_of_elements: tuple[int, int]):
        self.shape = shape
        self.range_of_elements = range_of_elements
        elements = np.prod(shape)
        range_size = range_of_elements[1] - range_of_elements[0]
        self.max_hash = range_size**elements
        x = np.arange(elements)
        self._higher_base = (range_size**(x+1)).reshape(shape)
        self._lower_base = (range_size**x).reshape(shape)
    
    def hash_to_state(self, hash: int) -> np.ndarray:
        state = hash % self._higher_base // self._lower_base
        return state

    def state_to_hash(self, state: np.ndarray) -> int:
        hash = np.sum(state * self._lower_base)
        return hash