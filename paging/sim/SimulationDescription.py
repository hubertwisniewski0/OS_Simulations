from typing import List
from utils.Serializable import Serializable


class SimulationDescription(Serializable):
    memory_sizes: List[int]
    access_list: List[int]

    def serialize(self):
        return {
            "memory_sizes": self.memory_sizes,
            "access_list": self.access_list
        }
