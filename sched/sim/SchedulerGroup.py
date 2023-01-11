from typing import Dict
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
        self.schedulers["FCFS"] = SchedulerFCFS(self.simulation.task_list)
        self.schedulers["SJF"] = SchedulerSJF(self.simulation.task_list)
        self.schedulers["Lottery"] = SchedulerLottery(self.simulation.task_list, self.simulation.lottery_seed)

        for scheduler in self.schedulers.values():
            while scheduler.tick():
                pass

    def serialize(self):
        return self.schedulers
