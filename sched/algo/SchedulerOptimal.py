import sys
from typing import Optional, List
from ..core.Scheduler import Scheduler
from ..core.Task import Task


class SchedulerOptimal(Scheduler):
    def __init__(self, task_list: List[Task]):
        super().__init__(task_list)

        self.task_list.sort(key=lambda t: t.duration)
        self.optimal_order: List[Task] = []
        self.best_turnaround_time = None

        self.recurse_tasks([], 0, 0)
        print(self.best_turnaround_time / len(self.task_list) if self.best_turnaround_time else None, file=sys.stderr)

    def recurse_tasks(self, starting_point: List[Task], passed_time: int, accumulated_turnaround_time: int):
        if self.best_turnaround_time and accumulated_turnaround_time >= self.best_turnaround_time:
            return

        assert len(starting_point) <= len(self.task_list)

        if len(starting_point) == len(self.task_list) and (
                not self.best_turnaround_time or accumulated_turnaround_time < self.best_turnaround_time):
            self.best_turnaround_time = accumulated_turnaround_time
            self.optimal_order = starting_point
            return

        remaining_tasks = [task for task in self.task_list if task not in starting_point]
        for task in remaining_tasks:
            task_end_time = max(passed_time, task.come_time) + task.duration
            self.recurse_tasks(starting_point + [task], task_end_time,
                               accumulated_turnaround_time + task_end_time - task.come_time)

    def select_next_task(self) -> Optional[Task]:
        if self.optimal_order[0] in self.waiting_tasks:
            self.waiting_tasks.remove(self.optimal_order[0])
            return self.optimal_order.pop(0)
        return None
