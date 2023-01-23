from random import Random
from typing import Optional, List

from ..core.Scheduler import Scheduler
from ..core.Task import Task


class SchedulerLottery(Scheduler):
    """
    Lottery scheduling algorithm implementation
    """

    def __init__(self, task_list: List[Task], seed: Optional[int]):
        """
        :param task_list: list of tasks to process
        :param seed: seed for the random number generator or `None` to use the current system time
        """
        super().__init__(task_list)
        self.rng = Random(seed)

    def select_next_task(self) -> Optional[Task]:
        if len(self.waiting_tasks) == 0:
            return None

        # Select a random waiting task
        self.rng.shuffle(self.waiting_tasks)
        return self.waiting_tasks.pop(0)
