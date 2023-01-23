from typing import Optional, List

from utils.Serializable import Serializable
from ..core.Task import Task


class SimulationDescription(Serializable):
    """
    Scheduler simulation description (data class)
    """
    # Seed for lotery algorithm implementation's RNG or `None` to use the current system time
    lottery_seed: Optional[int]

    # List of tasks to process
    task_list: List[Task]

    def serialize(self):
        return {
            "lottery_seed": self.lottery_seed,
            "task_list": self.task_list
        }
