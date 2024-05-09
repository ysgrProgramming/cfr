from .base import ExtensiveGame
from typing import Generator


class Disturb(ExtensiveGame):
    path_length: int
    p1_length: int
    p2_length: int
    late_time: int
    max_turn: int
    n: int

    def __init__(self, path_length: int, p1_length: int = 1, p2_length: int = 1, direction: list[int] = [-1, 0, 1], late_time: int = 2, max_turn: int = 10):
        self.n = 2
        self.path_length = path_length
        self.p1_length = p1_length
        self.p2_length = p2_length
        self.direction = direction
        self.late_time = late_time
        self.max_turn = max_turn

    def get_actions(self, history: list[int] = []) -> Generator[int, None, None]:
        if self.get_active_player(history) == 0:
            p_length = self.p1_length
        else:
            p_length = self.p2_length
        
        if len(history) >= 2:
            last_action = history[-2]
            for d in self.direction:
                action = last_action + d
                if 0 <= action < self.path_length-p_length:
                    yield action
        else:
            yield (self.path_length-p_length)//2

    def get_active_player(self, history: list[int]) -> int:
        return len(history) % 2

    def get_information_tuple(self, history: list[int]) -> tuple[int]:
        player_history = [history[i] for i in range(-1, -2*(self.late_time+1), -2) if i > -len(history)]
        if 1+2*self.late_time < len(history):
            enemy_history = [history[-1-2*self.late_time]]
        else:
            enemy_history = []
        info_tuple = tuple(player_history + enemy_history + [len(history)])
        return info_tuple

    def get_utility(self, history: list[int]) -> tuple[float] | None:
        if len(history) == self.max_turn*2:
            player_history = [h for h in history[0::2]]
            enemy_history = [h for h in history[1::2]]
            point = 0
            for h1, h2 in zip(player_history, enemy_history):
                if h1 == h2: point += 1
            return (point/self.max_turn, -point/self.max_turn)