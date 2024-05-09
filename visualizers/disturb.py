from .base import Visualizer
from extensive_games import Disturb
from strategy import Strategy
import random

class DisturbVisualizer(Visualizer):
    def __init__(self, game: Disturb, strategy: Strategy):
        self.game = game
        self.strategy = strategy

    def visualize(self, history):
        if len(history) == 0 or len(history) % 2 == 1: return
        p1_pos = history[-2]
        p2_pos = history[-1]
        p1_length = self.game.p1_length
        p2_length = self.game.p2_length
        length = self.game.path_length
        print("Turn:", len(history))
        print("Player 1:", "."*p1_pos + "x"*p1_length + "." + "."*(length - p1_pos+p1_length))
        print("Player 2:", "."*p2_pos + "x"*p2_length + "." + "."*(length - p2_pos+p2_length))
        print()

    def random(self):
        history = []
        while self.game.get_utility(history) is None:
            info = self.game.get_information_tuple(history)
            info_idx = self.strategy.info_dict[info]
            hand = random.choices(self.strategy.info_to_action_graph[info_idx], weights=self.strategy.dstb_list[info_idx], k=1)[0]
            history.append(hand)
            self.visualize(history)