import json
from typing import List, Dict
from numpy import average
from concurrent.futures import ProcessPoolExecutor, Future
from .SimulationDescription import SimulationDescription
from .MemoryManagerGroup import MemoryManagerGroup
from .SimulationPlotter import SimulationPlotter
from utils.Serializable import Serializable


class MemoryManagerSimulation(Serializable):
    def __init__(self, jobs: int):
        self.memory_manager_groups: List[MemoryManagerGroup] = []
        self.simulations: List[SimulationDescription] = []
        self.average_page_faults: Dict[str, float] = {}
        self.jobs = jobs

    def read_data(self, input_file_name: str):
        with open(input_file_name, 'rt') as f:
            input_data = json.load(f)

        for item in input_data:
            desc = SimulationDescription()
            desc.memory_sizes = item["memory_sizes"]
            desc.access_list = item["access_list"]

            self.simulations.append(desc)

    def simulate(self):
        futures: List[Future] = []
        with ProcessPoolExecutor(max_workers=self.jobs) as executor:
            for simulation in self.simulations:
                memory_manager_group = MemoryManagerGroup(simulation)
                self.memory_manager_groups.append(memory_manager_group)
                futures.append(executor.submit(memory_manager_group.simulate))

        for i in range(len(futures)):
            self.memory_manager_groups[i] = futures[i].result()

        self.generate_stats()

    def create_plot(self, output_file: str):
        plotter = SimulationPlotter()
        plotter.generate_plot(self.memory_manager_groups)
        plotter.save_plot(output_file)

    def generate_stats(self):
        page_faults: Dict[str, List[int]] = {}

        for mm_group in self.memory_manager_groups:
            for mm_name, mm in mm_group.memory_managers.items():
                if mm_name not in page_faults.keys():
                    page_faults[mm_name] = []

                page_faults[mm_name].append(mm.page_faults)

        for mm_name, page_fault_counts in page_faults.items():
            self.average_page_faults[mm_name] = average(page_fault_counts)

    def serialize(self):
        return {
            "average_page_faults": self.average_page_faults,
            "memory_manager_groups": self.memory_manager_groups
        }
