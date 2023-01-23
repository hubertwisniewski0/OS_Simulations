from typing import List
from utils.Serializable import Serializable


class SimulationDescription(Serializable):
    """
    Paging simulation description (data class)
    """
    # Memory sizes (in pages) to simulate
    memory_sizes: List[int]

    # List of page access requests
    access_list: List[int]

    def serialize(self):
        return {
            "memory_sizes": self.memory_sizes,
            "access_list": self.access_list
        }
