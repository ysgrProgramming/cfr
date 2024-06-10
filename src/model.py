from .extensive_games import ExtensiveGame
from dataclasses import dataclass
from .util import StateHashConverter

import sys

class Model():
    def __init__(self, game):
        sys.setrecursionlimit(10**9)
        self.dinfo_list: list[tuple[int]] = []
        self.dinfo_to_node_dict: dict[tuple[int], int] = {}
        self.node_to_utility_list: list[int | None] = []
        self.node_to_player_list: list[int | None] = []
        self.info_list: list[int] = []
        self.info_to_idx_dict: dict[int, int] = {}
        self.idx_to_nodes_list: list[set[int]] = []
        self.graph: list[list[int]] = []
        self.game = game

    def search(self, game):
        conv = StateHashConverter(game.init_state.shape, game.range_of_elements)
        init_state = game.init_state
        self._search(init_state, 1, game, conv)
    
    def _search(self, state, player, game: ExtensiveGame, conv:StateHashConverter):
        #print(state)
        hash1 = conv.state_to_hash(state[0])
        hash2 = conv.state_to_hash(state[1])
        dhash = (hash1, hash2)
        if dhash in self.dinfo_to_node_dict:
            node_idx = self.dinfo_to_node_dict[dhash]
            return node_idx
        self.dinfo_list.append(dhash)
        node_idx = len(self.dinfo_list)-1
        self.dinfo_to_node_dict[dhash] = node_idx
        if hash1 not in self.info_to_idx_dict:
            self.info_list.append(hash1)
            self.idx_to_nodes_list.append(set())
            info1_idx = len(self.info_list)-1
            self.info_to_idx_dict[hash1] = info1_idx
        else:
            info1_idx = self.info_to_idx_dict[hash1]
        if hash2 not in self.info_to_idx_dict:
            self.info_list.append(hash2)
            self.idx_to_nodes_list.append(set())
            info2_idx = len(self.info_list)-1
            self.info_to_idx_dict[hash2] = info2_idx
        else:
            info2_idx = self.info_to_idx_dict[hash2]
        
        self.idx_to_nodes_list[info1_idx].add(node_idx)
        self.idx_to_nodes_list[info2_idx].add(node_idx)

        utility = game.evaluate_state(state)
        self.node_to_utility_list.append(utility)
        self.node_to_player_list.append(player)

        self.graph.append([])
        if utility == None:
            for next_state, next_player in game.find_next_states(state, player):
                next_node_idx = self._search(next_state, next_player, game, conv)
                self.graph[node_idx].append(next_node_idx)
        
        return node_idx