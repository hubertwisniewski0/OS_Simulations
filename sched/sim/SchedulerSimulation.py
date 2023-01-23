import json
from typing import List, Dict, Tuple
from numpy import average
from concurrent.futures import ProcessPoolExecutor
from .SchedulerGroup import SchedulerGroup
from .SimulationDescription import SimulationDescription
from .SimulationPlotter import SimulationPlotter
from ..core.TaskFactory import TaskFactory
from utils.Serializable import Serializable


class SchedulerSimulation(Serializable):
    """
    Responsible for reading input data, performing all simulations and drawing plots
    """
    def __init__(self, jobs: int, enable_optimal: bool):
        """
        :param jobs: maximum number of concurrent simulations or `None` to determine automatically
        :param enable_optimal: whether to enable optimal algorithm
        """
        self.scheduler_groups: List[SchedulerGroup] = []
        self.simulations: List[SimulationDescription] = []
        self.jobs = jobs
        self.enable_optimal = enable_optimal
        self.average_waiting_times: Dict[str, float] = {}
        self.average_turnaround_times: Dict[str, float] = {}

    def read_data(self, input_file_name: str):
        """
        Read simulation data from file
        :param input_file_name: name of the file to read
        """
        with open(input_file_name, 'rt') as f:
            input_data = json.load(f)

        for item in input_data:
            desc = SimulationDescription()
            desc.lottery_seed = item["lottery_seed"]

            task_factory = TaskFactory()
            desc.task_list = [task_factory.create_task(task["come_time"], task["duration"]) for task in
                              item["task_list"]]

            self.simulations.append(desc)

    @staticmethod
    def simulation_worker(parameters: Tuple[SimulationDescription, bool]) -> SchedulerGroup:
        """
        Worker function responsible for creating and running a single simulation group. Meant to be run concurrently.
        :param parameters: simulation parameters:
            Tuple[
                simulation: SimulationDescription,
                enable_optimal: bool // whether to enable optimal algorithm
            ]
        :return: scheduler group after performing all simulations from the provided simulation description
        """
        simulation, enable_optimal = parameters
        sched_group = SchedulerGroup(simulation, enable_optimal)
        sched_group.create_schedulers()
        sched_group.simulate()
        return sched_group

    def simulate(self):
        """
        Concurrently perform all simulation groups
        """
        with ProcessPoolExecutor(max_workers=self.jobs) as executor:
            self.scheduler_groups = [scheduler_group for scheduler_group in
                                     executor.map(self.simulation_worker,
                                                  zip(self.simulations, iter(lambda: self.enable_optimal, None)))]

    def create_plot(self, output_file: str):
        """
        Create plot based on simulation output date and save it to file
        :param output_file: name of the file to save the plot to
        """
        plotter = SimulationPlotter()
        plotter.generate_plot(self.scheduler_groups)
        plotter.save_plot(output_file)

    def generate_stats(self):
        """
        Generate global average waiting and turnaround time statistic
        """
        waiting_times: Dict[str, List[int]] = {}
        turnaround_times: Dict[str, List[int]] = {}

        # Collect data from complete simulations
        for sched_group in self.scheduler_groups:
            for sched_name, sched in sched_group.schedulers.items():
                if sched_name not in waiting_times.keys():
                    waiting_times[sched_name] = []
                if sched_name not in turnaround_times.keys():
                    turnaround_times[sched_name] = []

                waiting_times[sched_name] += sched.task_waiting_times
                turnaround_times[sched_name] += sched.task_turnaround_times

        for sched_name, waiting_times_list in waiting_times.items():
            self.average_waiting_times[sched_name] = average(waiting_times_list)

        for sched_name, turnaround_times_list in turnaround_times.items():
            self.average_turnaround_times[sched_name] = average(turnaround_times_list)

    def serialize(self):
        return {
            "average_waiting_times": self.average_waiting_times,
            "average_turnaround_times": self.average_turnaround_times,
            "scheduler_groups": self.scheduler_groups
        }
