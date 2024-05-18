from .extensive_games import ExtensiveGame
from dataclasses import dataclass
from .util import StateHashConverter

@dataclass
class Model():
    def __init__(self):
        self.dinfo_list: list[tuple[int]] = []
        self.dinfo_to_node_dict: dict[tuple[int], int] = dict()
        self.node_to_utility_list: list[int | None] = list()
        self.info_list: list[int] = list()
        self.info_to_idx_dict: dict[int, int] = dict()
        self.idx_to_nodes_dict: dict[int, list[int]] = dict()
        self.graph: list[list[int]] = list()
    
    def search(self, game):
        conv = StateHashConverter(game.init_state.shape, game.range_of_elements)
        init_state = game.init_state
        self._search(self, init_state, game, conv)
    
    def _search(self, state, game: ExtensiveGame, conv:StateHashConverter):
        hash1 = conv.state_to_hash(state[0])
        hash2 = conv.state_to_hash(state[1])
        dhash = (hash1, hash2)
        if dhash not in self.dinfo_to_node_dict:
            pass