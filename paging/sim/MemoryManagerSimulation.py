import json
from typing import List
from .SimulationDescription import SimulationDescription
from .MemoryManagerGroup import MemoryManagerGroup
from utils.Serializable import Serializable


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
