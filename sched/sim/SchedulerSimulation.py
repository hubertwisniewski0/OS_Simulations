import json
from typing import List
from .SchedulerGroup import SchedulerGroup
from .SimulationDescription import SimulationDescription
from .SimulationPlotter import SimulationPlotter
from ..core.TaskFactory import TaskFactory
from utils.Serializable import Serializable


class SchedulerSimulation(Serializable):
    def __init__(self):
        self.scheduler_groups: List[SchedulerGroup] = []
        self.simulations: List[SimulationDescription] = []

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
        for simulation in self.simulations:
            sched_group = SchedulerGroup(simulation)
            self.scheduler_groups.append(sched_group)
            sched_group.simulate()

    def create_plot(self, output_file: str):
        plotter = SimulationPlotter()
        plotter.generate_plot(self.scheduler_groups)
        plotter.save_plot(output_file)

    def serialize(self):
        return self.scheduler_groups
