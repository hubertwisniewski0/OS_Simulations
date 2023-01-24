from typing import List

from utils.Serializable import Serializable


class SimulationDescription(Serializable):
    """
    Paging simulation description (data class)
    """

    memory_sizes: List[int]
    """
    Memory sizes (in pages) to simulate
    """

    access_list: List[int]
    """
    List of page access requests
    """

    def serialize(self):
        return {
            "memory_sizes": self.memory_sizes,
            "access_list": self.access_list
        }
