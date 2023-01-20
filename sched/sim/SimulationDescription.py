from typing import Optional, List
from ..core.Task import Task
from utils.Serializable import Serializable


class SimulationDescription(Serializable):
    lottery_seed: Optional[int]
    task_list: List[Task]

    def serialize(self):
        return {
            "lottery_seed": self.lottery_seed,
            "task_list": self.task_list
        }
