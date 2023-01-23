from typing import Optional
from ..core.Scheduler import Scheduler
from ..core.Task import Task


class SchedulerSJF(Scheduler):
    """
    Shortest Job First scheduling algorithm implementation
    """
    def select_next_task(self) -> Optional[Task]:
        if len(self.waiting_tasks) == 0:
            return None

        # Sort tasks by their duration in such a way that tasks with the same duration are ordered by their ID
        self.waiting_tasks.sort(key=lambda task: task.task_id)
        self.waiting_tasks.sort(key=lambda task: task.duration)

        # Return the shortest waiting task
        return self.waiting_tasks.pop(0)
