from typing import Optional, List

from utils.Serializable import Serializable
from ..core.Task import Task


class SimulationDescription(Serializable):
    """
    Scheduler simulation description (data class)
    """

    lottery_seed: Optional[int]
    """
    Seed for lottery algorithm implementation's RNG or `None` to use the current system time
    """

    task_list: List[Task]
    """
    List of tasks to process
    """

    def serialize(self):
        return {
            "lottery_seed": self.lottery_seed,
            "task_list": self.task_list
        }
