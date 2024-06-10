from .base import StrategyMaker
from ..model import Model


class CFR:
    def __init__(self, model: Model, t):
        self.model = model
        self.t = t
        self.regret_tables = [[[0]*len(model.graph[next(iter(nodes))]) for nodes in model.idx_to_nodes_list] for _ in range(t+1)]
        self.strategy_tables = [[[1/max(1, len(model.graph[next(iter(nodes))]))]*len(model.graph[next(iter(nodes))]) for nodes in model.idx_to_nodes_list] for _ in range(t)]
        self.mean_strategy_tables = None
    
    def analyze(self, t):
        for i in range(t):
            for j in range(1, 3):
                print(f"analyzing {i}, {j}")
                self._analyze(0, j, i, 1, 1)
        self.mean_strategy_tables 
    
    def _analyze(self, node_idx, player, t, pi1, pi2):
        utility = self.model.node_to_utility_list[node_idx]
        regret_table = [[0]*len(self.model.graph[next(iter(nodes))]) for nodes in self.model.idx_to_nodes_list]
        strategy_table = [[1/max(1, len(self.model.graph[next(iter(nodes))]))]*len(self.model.graph[next(iter(nodes))]) for nodes in self.model.idx_to_nodes_list]
        if utility != None:
            return utility
        info = self.model.dinfo_list[node_idx][player-1]
        info_idx = self.model.info_to_idx_dict[info]
        regret_sum = sum(max(r, 0) for r in self.regret_tables[t][info_idx])
        if regret_sum > 0:
            for i, regret in enumerate(self.regret_tables[t][info_idx]):
                strategy_table[info][i] = max(regret, 0)/regret_sum
        all_v = 0
        v_list = [0]*len(regret_table[info_idx])
        for i in range(len(regret_table[info_idx])):
            next_node_idx = self.model.graph[node_idx][i]
            if self.model.node_to_player_list[node_idx] == player:
                v_list[i] = self._analyze(next_node_idx, player, t, strategy_table[info_idx][i]*pi1, pi2)
            else:
                v_list[i] = self._analyze(next_node_idx, player, t, pi1, strategy_table[info_idx][i]*pi2)
            all_v += strategy_table[info_idx][i]*v_list[i]
        return all_v
