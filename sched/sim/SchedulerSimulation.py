import json
from typing import List
from .SchedulerGroup import SchedulerGroup
from .SimulationDescription import SimulationDescription
from ..core.Task import Task
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
            desc.task_list = []

            # TODO: Task factory
            task_id_counter = 0
            for task in item["task_list"]:
                desc.task_list.append(Task(task_id_counter, task["come_time"], task["duration"]))
                task_id_counter += 1

            self.simulations.append(desc)

    def simulate(self):
        for simulation in self.simulations:
            sched_group = SchedulerGroup(simulation)
            self.scheduler_groups.append(sched_group)
            sched_group.simulate()

    def serialize(self):
        return self.scheduler_groups
