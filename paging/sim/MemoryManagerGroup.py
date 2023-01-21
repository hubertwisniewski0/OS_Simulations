from typing import Dict
from .SimulationDescription import SimulationDescription
from ..core import MemoryManager
from ..algo.MemoryManagerFIFO import MemoryManagerFIFO
from ..algo.MemoryManagerLFU import MemoryManagerLFU
from ..algo.MemoryManagerMFU import MemoryManagerMFU
from ..algo.MemoryManagerOptimal import MemoryManagerOptimal
from utils.Serializable import Serializable


class MemoryManagerGroup(Serializable):
    def __init__(self, simulation: SimulationDescription):
        self.simulation = simulation
        self.memory_managers: Dict[str, MemoryManager] = {}

    def simulate(self):
        for memory_size in self.simulation.memory_sizes:
            self.memory_managers["_".join(["FIFO", str(memory_size)])] =\
                MemoryManagerFIFO(self.simulation.access_list, memory_size)
            self.memory_managers["_".join(["LFU", str(memory_size)])] =\
                MemoryManagerLFU(self.simulation.access_list, memory_size)
            self.memory_managers["_".join(["MFU", str(memory_size)])] =\
                MemoryManagerMFU(self.simulation.access_list, memory_size)
            self.memory_managers["_".join(["Optimal", str(memory_size)])] =\
                MemoryManagerOptimal(self.simulation.access_list, memory_size)

        for memory_manager in self.memory_managers.values():
            memory_manager.process_all()

        return self

    def serialize(self):
        return self.memory_managers
