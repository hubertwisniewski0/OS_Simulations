from typing import Optional

from ..core.Scheduler import Scheduler
from ..core.Task import Task


class SchedulerFCFS(Scheduler):
    """
    First Come First Serve scheduling algorithm implementation
    """

    def select_next_task(self) -> Optional[Task]:
        if len(self.waiting_tasks) == 0:
            return None

        # Sort tasks by their come time in such a way that tasks with the same come time are ordered by their ID
        self.waiting_tasks.sort(key=lambda task: task.task_id)
        self.waiting_tasks.sort(key=lambda task: task.come_time)

        # Return the first task to come
        return self.waiting_tasks.pop(0)
