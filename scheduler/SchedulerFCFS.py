from typing import Optional
from scheduler.Scheduler import Scheduler
from scheduler.Task import Task


class SchedulerFCFS(Scheduler):
    def select_next_task(self) -> Optional[Task]:
        if len(self.waiting_tasks) == 0:
            return None

        self.waiting_tasks.sort(key=lambda task: task.task_id)
        self.waiting_tasks.sort(key=lambda task: task.come_time)

        return self.waiting_tasks.pop(0)
