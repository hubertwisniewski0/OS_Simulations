import json
from typing import Dict, List
from utils.Serializable import Serializable
from .MemoryManager import MemoryManager
from .MemoryManagerFIFO import MemoryManagerFIFO
from .MemoryManagerLFU import MemoryManagerLFU
from .MemoryManagerMFU import MemoryManagerMFU
from .MemoryManagerOptimal import MemoryManagerOptimal


class SimulationDescription:
    memory_sizes: List[int]
    access_list: List[int]


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

    def serialize(self):
        return self.memory_managers


class MemoryManagerSimulation(Serializable):
    def __init__(self):
        self.memory_manager_groups: List[MemoryManagerGroup] = []
        self.simulations: List[SimulationDescription] = []

    def read_data(self, input_file_name: str):
        with open(input_file_name, 'rt') as f:
            input_data = json.load(f)

        for item in input_data:
            desc = SimulationDescription()
            desc.memory_sizes = item["memory_sizes"]
            desc.access_list = item["access_list"]

            self.simulations.append(desc)

    def simulate(self):
        for simulation in self.simulations:
            memory_manager_group = MemoryManagerGroup(simulation)
            self.memory_manager_groups.append(memory_manager_group)
            memory_manager_group.simulate()

    def serialize(self):
        return self.memory_manager_groups
