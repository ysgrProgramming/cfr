from .base import ExtensiveGame
import numpy as np

class Daruma(ExtensiveGame):
    def __init__(self, red_time, green_time, distance, late):
        last_action = 0
        ally_list = [red_time, green_time, distance, 0, 0]
        enemy_list = [red_time, green_time, distance, last_action, 1]
        self.init_state = np.array([ally_list, enemy_list])
        self.range_of_elements = (0, max(red_time+1, green_time+1))
        self.distance = distance
        self.late = late
    
    def find_next_states(self, state, player):
        if player == 1:
            #stop
            new_state = state.copy()
            new_state[0][3] = state[1][3]
            yield new_state, 2
            #go
            new_state = state.copy()
            if state[1][3] == 1:
                new_state[0][2] -= 1
            else:
                new_state[0][2] -= 1
            yield new_state, 2
        elif player == 2:
            #look
            new_state = state.copy()
            if state[1][0] > 0:
                new_state[1][0] -= 1
                new_state[0][0] -= 1
                new_state[1][2] = state[0][2]
                new_state[1][3] = 1
                yield new_state, 1
            #hide
            new_state = state.copy()
            new_state[1][1] -= 1
            new_state[0][1] -= 1
            new_state[1][3] = 0
            yield new_state, 1

    def find_mirror_states(self, state):
        yield state
    
    def evaluate_state(self, state):
        if state[1][1] == 0: return (-1, 1)
        elif state[0][2] == 0: return (1, -1)
        else: return None