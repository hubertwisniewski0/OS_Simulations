import json
import sys
from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict, Optional

from numpy import average

from utils.Serializable import Serializable
from .MemoryManagerGroup import MemoryManagerGroup
from .SimulationDescription import SimulationDescription
from .SimulationPlotter import SimulationPlotter


class MemoryManagerSimulation(Serializable):
    """
    Responsible for reading input data, performing all simulations and drawing plots
    """

    def __init__(self, jobs: Optional[int]):
        """
        :param jobs: maximum number of concurrent simulations or `None` to determine automatically
        """
        self.memory_manager_groups: List[MemoryManagerGroup] = []
        self.simulations: List[SimulationDescription] = []
        self.average_page_faults: Dict[str, float] = {}
        self.jobs = jobs

    def read_data(self, input_file_name: str):
        """
        Read simulation data from file
        :param input_file_name: name of the file to read
        """
        with open(input_file_name, 'rt') as f:
            input_data = json.load(f)

        for item in input_data:
            desc = SimulationDescription()
            desc.memory_sizes = item["memory_sizes"]
            desc.access_list = item["access_list"]

            self.simulations.append(desc)

    @staticmethod
    def simulation_worker(simulation: SimulationDescription) -> MemoryManagerGroup:
        """
        Worker function responsible for creating and running a single simulation group. Meant to be run concurrently.
        :param simulation: simulation description
        :return: memory manager group after performing all simulations from the provided simulation description
        """
        mm_group = MemoryManagerGroup(simulation)
        mm_group.create_managers()
        mm_group.simulate()
        return mm_group

    def simulate(self):
        """
        Concurrently perform all simulation groups
        """
        with ProcessPoolExecutor(max_workers=self.jobs) as executor:
            for memory_manager_group in executor.map(self.simulation_worker, self.simulations):
                self.memory_manager_groups.append(memory_manager_group)
                print('Simulations complete: {}/{}'.format(len(self.memory_manager_groups), len(self.simulations)),
                      file=sys.stderr)

    def create_plot(self, output_file: str):
        """
        Create plot based on simulation output date and save it to file
        :param output_file: name of the file to save the plot to
        """
        plotter = SimulationPlotter()
        plotter.generate_plot(self.memory_manager_groups)
        plotter.save_plot(output_file)

    def generate_stats(self):
        """
        Generate average page faults statistic
        """
        page_faults: Dict[str, List[int]] = {}

        # Collect data from complete simulations
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
