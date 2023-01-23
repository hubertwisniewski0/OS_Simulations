from typing import Dict

from utils.Serializable import Serializable
from .SimulationDescription import SimulationDescription
from ..algo.MemoryManagerFIFO import MemoryManagerFIFO
from ..algo.MemoryManagerLFU import MemoryManagerLFU
from ..algo.MemoryManagerMFU import MemoryManagerMFU
from ..algo.MemoryManagerOptimal import MemoryManagerOptimal
from ..core import MemoryManager


class MemoryManagerGroup(Serializable):
    """
    Group of memory managers performing simulations based on the same input data
    """

    def __init__(self, simulation: SimulationDescription):
        """
        :param simulation: simulation description
        """
        self.simulation = simulation
        self.memory_managers: Dict[str, MemoryManager] = {}

    def create_managers(self):
        """
        Create all memory managers for all memory sizes
        """
        for memory_size in self.simulation.memory_sizes:
            self.memory_managers["_".join(["FIFO", str(memory_size)])] = \
                MemoryManagerFIFO(self.simulation.access_list, memory_size)
            self.memory_managers["_".join(["LFU", str(memory_size)])] = \
                MemoryManagerLFU(self.simulation.access_list, memory_size)
            self.memory_managers["_".join(["MFU", str(memory_size)])] = \
                MemoryManagerMFU(self.simulation.access_list, memory_size)
            self.memory_managers["_".join(["Optimal", str(memory_size)])] = \
                MemoryManagerOptimal(self.simulation.access_list, memory_size)

    def simulate(self):
        """
        Perform all simulations
        """
        for memory_manager in self.memory_managers.values():
            memory_manager.process_all()

    def serialize(self):
        return self.memory_managers
