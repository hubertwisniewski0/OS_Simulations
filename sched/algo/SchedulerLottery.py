from random import Random
from typing import Optional, List
from ..core.Scheduler import Scheduler
from ..core.Task import Task


class SchedulerLottery(Scheduler):
    def __init__(self, task_list: List[Task], seed: Optional[int]):
        super().__init__(task_list)
        self.rng = Random(seed)

    def select_next_task(self) -> Optional[Task]:
        if len(self.waiting_tasks) == 0:
            return None

        self.rng.shuffle(self.waiting_tasks)
        return self.waiting_tasks.pop(0)
