import json
from copy import deepcopy
from typing import Optional, List, Dict
from .Scheduler import Scheduler
from .SchedulerFCFS import SchedulerFCFS
from .SchedulerLottery import SchedulerLottery
from .SchedulerSJF import SchedulerSJF
from .Task import Task
from utils.Serializable import Serializable


class SimulationDescription:
    lottery_seed: Optional[int]
    task_list: List[Task]


class SchedulerGroup(Serializable):
    def __init__(self, simulation: SimulationDescription):
        self.simulation = simulation
        self.schedulers: Dict[str, Scheduler] = {}

    def simulate(self):
        self.schedulers["FCFS"] = SchedulerFCFS(deepcopy(self.simulation.task_list))
        self.schedulers["SJF"] = SchedulerSJF(deepcopy(self.simulation.task_list))
        self.schedulers["Lottery"] = SchedulerLottery(deepcopy(self.simulation.task_list), self.simulation.lottery_seed)

        for scheduler in self.schedulers.values():
            while scheduler.tick():
                pass

    def serialize(self):
        return self.schedulers


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
