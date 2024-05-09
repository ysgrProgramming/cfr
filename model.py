from pydantic import BaseModel
from extensive_games import ExtensiveGame
from dataclasses import dataclass

@dataclass
class Model():
    n: int
    info_dict: dict[tuple[int], int]
    node_to_info_list: list[int]
    info_to_node_list: list[set[int]]
    info_to_player_list: list[int]
    info_to_utility_list: list[int | None]
    info_to_action_graph: list[list[int]]
    graph: list[list[int]]
    
    def __init__(self, game: ExtensiveGame):
        self.n = game.n
        self.info_dict: dict[tuple[int], int] = dict()
        self.node_to_info_list: list[int] = []
        self.info_to_node_list: list[set[int]] = []
        self.info_to_player_list: list[int] = []
        self.info_to_utility_list: list[tuple[float] | None] = []
        self.info_to_action_graph: list[list[int]] = []
        self.graph: list[list[int]] = []
        self._search(game)
    
    def _search(self, game: ExtensiveGame, history: list[int] = []):
        idx = len(self.graph)
        info = game.get_information_tuple(history)
        if info in self.info_dict:
            info_idx = self.info_dict[info]
            self.info_to_node_list[info_idx].add(idx)
            actions = self.info_to_action_graph[info_idx]
            utility = self.info_to_utility_list[info_idx]
        else:
            info_idx = len(self.info_dict)
            self.info_dict[info] = info_idx
            self.info_to_node_list.append({idx})
            utility = game.get_utility(history)
            if utility == None:
                actions = list(game.get_actions(history))
                player = game.get_active_player(history)
            else:
                actions = []
                player = -1
            self.info_to_utility_list.append(utility)
            self.info_to_player_list.append(player)
            self.info_to_action_graph.append(actions)
        self.node_to_info_list.append(info_idx)

        child_list = []
        for action in actions:
            history.append(action)
            child_idx = self._search(game, history)
            child_list.append(child_idx)
            history.pop()
        self.graph.append(child_list)
        return idx