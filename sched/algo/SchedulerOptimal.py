import sys
from typing import Optional, List
from ..core.Scheduler import Scheduler
from ..core.Task import Task


class SchedulerOptimal(Scheduler):
    def __init__(self, task_list: List[Task]):
        super().__init__(task_list)

        self.task_list.sort(key=lambda t: t.duration)
        self.optimal_order: List[Task] = []
        self.best_turnaround_time = -1

        self.recurse_tasks([], 0, 0)
        print(self.best_turnaround_time/len(self.task_list), file=sys.stderr)

    def recurse_tasks(self, starting_point: List[Task], passed_time: int, accumulated_turnaround_time: int):
        if -1 < self.best_turnaround_time <= accumulated_turnaround_time:
            return

        assert len(starting_point) <= len(self.task_list)

        if len(starting_point) == len(self.task_list) and (
                accumulated_turnaround_time < self.best_turnaround_time or self.best_turnaround_time < 0):
            self.best_turnaround_time = accumulated_turnaround_time
            self.optimal_order = starting_point
            return

        remaining_tasks = [task for task in self.task_list if task not in starting_point]
        if self.edd_heuristic_bound(remaining_tasks) > self.best_turnaround_time > -1:
            return

        for task in remaining_tasks:
            task_end_time = max(passed_time, task.come_time) + task.duration
            self.recurse_tasks(starting_point + [task], task_end_time,
                               accumulated_turnaround_time + task_end_time - task.come_time)

    @staticmethod
    def edd_heuristic_bound(task_list: List[Task]) -> int:
        # Sort tasks by their earliest due date
        task_list_ = sorted(task_list, key=lambda t: t.come_time + t.duration)

        total_turnaround_time = 0
        time_counter = 0
        for task in task_list_:
            if task.come_time >= time_counter:
                time_counter = task.come_time + task.duration
                total_turnaround_time += task.duration
            else:
                time_counter += task.duration
                total_turnaround_time += time_counter - task.come_time

        return total_turnaround_time

    def select_next_task(self) -> Optional[Task]:
        if self.optimal_order[0] in self.waiting_tasks:
            self.waiting_tasks.remove(self.optimal_order[0])
            return self.optimal_order.pop(0)
        return None
