from .base import Visualizer
from ..extensive_games import Daruma
from ..strategy import Strategy
import random

class DarumaVisualizer(Visualizer):
    def __init__(self, game: Daruma, strategy: Strategy = None):
        self.game = game
        self.strategy = strategy

    def visualize(self, state):
        print(f"state: {state}")

    def random(self):
        state = self.game.init_state
        while self.game.evaluate_state(state) is None:
            self.visualize(state)
            state = random.choices([s for s in self.game.find_next_states(state)], k=1)[0]