from typing import Dict

from utils.Serializable import Serializable
from .SimulationDescription import SimulationDescription
from ..algo.SchedulerFCFS import SchedulerFCFS
from ..algo.SchedulerLottery import SchedulerLottery
from ..algo.SchedulerOptimal import SchedulerOptimal
from ..algo.SchedulerSJF import SchedulerSJF
from ..core.Scheduler import Scheduler


class SchedulerGroup(Serializable):
    """
    Group of schedulers performing simulations based on the same input data
    """

    def __init__(self, simulation: SimulationDescription, enable_optimal: bool):
        """
        :param simulation: simulation description
        :param enable_optimal: whether to enable optimal algorithm
        """
        self.simulation = simulation
        self.schedulers: Dict[str, Scheduler] = {}
        self.enable_optimal = enable_optimal

    def create_schedulers(self):
        """
        Create all enabled schedulers
        """
        self.schedulers["FCFS"] = SchedulerFCFS(self.simulation.task_list)
        self.schedulers["SJF"] = SchedulerSJF(self.simulation.task_list)
        self.schedulers["Lottery"] = SchedulerLottery(self.simulation.task_list, self.simulation.lottery_seed)
        if self.enable_optimal:
            self.schedulers["Optimal"] = SchedulerOptimal(self.simulation.task_list)

    def simulate(self):
        """
        Perform all simulations
        """
        for scheduler in self.schedulers.values():
            while scheduler.tick():
                pass

    def serialize(self):
        return self.schedulers
