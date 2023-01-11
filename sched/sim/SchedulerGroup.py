from typing import Dict
from copy import deepcopy
from .SimulationDescription import SimulationDescription
from ..core.Scheduler import Scheduler
from ..algo.SchedulerFCFS import SchedulerFCFS
from ..algo.SchedulerSJF import SchedulerSJF
from ..algo.SchedulerLottery import SchedulerLottery
from utils.Serializable import Serializable


class SchedulerGroup(Serializable):
    def __init__(self, simulation: SimulationDescription):
        self.simulation = simulation
        self.schedulers: Dict[str, Scheduler] = {}

    def simulate(self):
        # TODO: make deepcopy scheduler's responsibility
        self.schedulers["FCFS"] = SchedulerFCFS(deepcopy(self.simulation.task_list))
        self.schedulers["SJF"] = SchedulerSJF(deepcopy(self.simulation.task_list))
        self.schedulers["Lottery"] = SchedulerLottery(deepcopy(self.simulation.task_list), self.simulation.lottery_seed)

        for scheduler in self.schedulers.values():
            while scheduler.tick():
                pass

    def serialize(self):
        return self.schedulers
