import sys
from typing import Optional, List
from ..core.Scheduler import Scheduler
from ..core.Task import Task


class SchedulerOptimal(Scheduler):
    def __init__(self, task_list: List[Task]):
        super().__init__(task_list)

        self.task_list.sort(key=lambda t: t.come_time)
        self.optimal_order: List[Task] = []
        self.optimal_turnaround_time = -1
        self.predicted_passed_time = 0

        self.recurse_tasks([], 0, 0)
        print(self.predicted_passed_time, self.optimal_turnaround_time/len(self.task_list), sep='/', file=sys.stderr)

    def recurse_tasks(self, starting_point: List[Task], passed_time: int, accumulated_turnaround_time: int):
        if -1 < self.optimal_turnaround_time <= accumulated_turnaround_time:
            return

        assert len(starting_point) <= len(self.task_list)

        if len(starting_point) == len(self.task_list) and (
                accumulated_turnaround_time < self.optimal_turnaround_time or self.optimal_turnaround_time < 0):
            self.optimal_turnaround_time = accumulated_turnaround_time
            self.optimal_order = starting_point
            self.predicted_passed_time = passed_time
            return

        for task in [task for task in self.task_list if task not in starting_point]:
            task_end_time = max(passed_time, task.come_time) + task.duration
            self.recurse_tasks(starting_point + [task], task_end_time,
                               accumulated_turnaround_time + task_end_time - task.come_time)

    def select_next_task(self) -> Optional[Task]:
        if self.optimal_order[0] in self.waiting_tasks:
            self.waiting_tasks.remove(self.optimal_order[0])
            return self.optimal_order.pop(0)
        return None
