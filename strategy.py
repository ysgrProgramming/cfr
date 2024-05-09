from pydantic import BaseModel
from model import Model
from dataclasses import dataclass

@dataclass
class Strategy():
    info_dict: dict[tuple[int], int]
    info_to_action_graph: list[list[int]]
    dstb_list: list[int]

    def __init__(self, info_dict, info_to_action_graph, dstb_list):
        self.info_dict = info_dict
        self.info_to_action_graph = info_to_action_graph
        self.dstb_list = dstb_list
    
    @classmethod
    def from_model(cls, model: Model):
        info_dict = model.info_dict
        info_to_action_graph = model.info_to_action_graph
        dstb_list = []
        for actions in info_to_action_graph:
            action_size = len(actions)
            if action_size == 0: dstb = []
            else: dstb = [1/action_size]*action_size
            dstb_list.append(dstb)
        return cls(
            info_dict,
            info_to_action_graph,
            dstb_list
        )