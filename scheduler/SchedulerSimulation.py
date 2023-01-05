import json
from copy import deepcopy
from typing import Optional, List
from scheduler.SchedulerFCFS import SchedulerFCFS
from scheduler.SchedulerLottery import SchedulerLottery
from scheduler.SchedulerSJF import SchedulerSJF
from scheduler.Task import Task
from utils.Serializable import Serializable


class SimulationDescription:
    lottery_seed: Optional[int]
    task_list: List[Task]


class SchedulerGroup(Serializable):
    def __init__(self, simulation: SimulationDescription):
        self.simulation = simulation
        self.sched_fcfs: Optional[SchedulerFCFS] = None
        self.sched_sjf: Optional[SchedulerSJF] = None
        self.sched_lottery: Optional[SchedulerLottery] = None

    def simulate(self):
        self.sched_fcfs = SchedulerFCFS(deepcopy(self.simulation.task_list))
        self.sched_sjf = SchedulerSJF(deepcopy(self.simulation.task_list))
        self.sched_lottery = SchedulerLottery(deepcopy(self.simulation.task_list), self.simulation.lottery_seed)

        for sched in [self.sched_fcfs, self.sched_sjf, self.sched_lottery]:
            while sched.tick():
                pass

    def serialize(self):
        return {"FCFS": self.sched_fcfs,
                "SJF": self.sched_sjf,
                "Lottery": self.sched_lottery}


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
