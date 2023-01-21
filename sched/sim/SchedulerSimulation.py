import json
from typing import List
from concurrent.futures import ProcessPoolExecutor, Future
from .SchedulerGroup import SchedulerGroup
from .SimulationDescription import SimulationDescription
from .SimulationPlotter import SimulationPlotter
from ..core.TaskFactory import TaskFactory
from utils.Serializable import Serializable


class SchedulerSimulation(Serializable):
    def __init__(self, jobs: int, enable_optimal: bool):
        self.scheduler_groups: List[SchedulerGroup] = []
        self.simulations: List[SimulationDescription] = []
        self.jobs = jobs
        self.enable_optimal = enable_optimal

    def read_data(self, input_file_name: str):
        with open(input_file_name, 'rt') as f:
            input_data = json.load(f)

        for item in input_data:
            desc = SimulationDescription()
            desc.lottery_seed = item["lottery_seed"]

            task_factory = TaskFactory()
            desc.task_list = [task_factory.create_task(task["come_time"], task["duration"]) for task in
                              item["task_list"]]

            self.simulations.append(desc)

    def simulate(self):
        futures: List[Future] = []
        with ProcessPoolExecutor(max_workers=self.jobs) as executor:
            for simulation in self.simulations:
                sched_group = SchedulerGroup(simulation, self.enable_optimal)
                self.scheduler_groups.append(sched_group)
                futures.append(executor.submit(sched_group.simulate))

        for i in range(len(futures)):
            self.scheduler_groups[i] = futures[i].result()

    def create_plot(self, output_file: str):
        plotter = SimulationPlotter()
        plotter.generate_plot(self.scheduler_groups)
        plotter.save_plot(output_file)

    def serialize(self):
        return self.scheduler_groups
