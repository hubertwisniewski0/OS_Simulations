from typing import Dict
from .SimulationDescription import SimulationDescription
from ..core.Scheduler import Scheduler
from ..algo.SchedulerFCFS import SchedulerFCFS
from ..algo.SchedulerSJF import SchedulerSJF
from ..algo.SchedulerLottery import SchedulerLottery
from ..algo.SchedulerOptimal import SchedulerOptimal
from utils.Serializable import Serializable


class SchedulerGroup(Serializable):
    def __init__(self, simulation: SimulationDescription, enable_optimal: bool):
        self.simulation = simulation
        self.schedulers: Dict[str, Scheduler] = {}
        self.enable_optimal = enable_optimal

    def simulate(self):
        self.schedulers["FCFS"] = SchedulerFCFS(self.simulation.task_list)
        self.schedulers["SJF"] = SchedulerSJF(self.simulation.task_list)
        self.schedulers["Lottery"] = SchedulerLottery(self.simulation.task_list, self.simulation.lottery_seed)
        if self.enable_optimal:
            self.schedulers["Optimal"] = SchedulerOptimal(self.simulation.task_list)

        for scheduler in self.schedulers.values():
            while scheduler.tick():
                pass

        return self

    def serialize(self):
        return self.schedulers
