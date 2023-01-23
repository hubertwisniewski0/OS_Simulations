import sys
from typing import Optional, List
from ..core.Scheduler import Scheduler
from ..core.Task import Task


class SchedulerOptimal(Scheduler):
    """
    Optimal scheduling algorithm implementation based on a pseudo-brute-force (brute force with optimum comparison).
    Minimizes average task turnaround time.
    """

    def __init__(self, task_list: List[Task]):
        """
        :param task_list: list of tasks to process
        """
        super().__init__(task_list)

        # SJF is known to yield nearly the most optimal solution, so sort the task list like SJF would to find the
        # optimal solution faster
        self.task_list.sort(key=lambda t: t.duration)

        # List of tasks in optimal scheduling order
        self.optimal_order: List[Task] = []

        # Metric of the best solution found so far or `None` if no solution found yet
        self.best_turnaround_time = None

        self.recurse_tasks([], 0, 0)

        # For debugging
        print('Optimal solution found: ',
              self.best_turnaround_time / len(self.task_list) if self.best_turnaround_time else None, file=sys.stderr)

    def recurse_tasks(self, starting_point: List[Task], passed_time: int, accumulated_turnaround_time: int):
        """
        Recursively find the best solution
        :param starting_point: list of tasks selected so far
        :param passed_time: predicted time passed so far when executing tasks from `staring_point`
        :param accumulated_turnaround_time: cumulative task turnaround time for tasks from `starting_point`
        """
        # Turnaround time accumulates additively - if the time accumulated so far is greater than the best solution,
        # abandon this branch
        if self.best_turnaround_time and accumulated_turnaround_time >= self.best_turnaround_time:
            return

        assert len(starting_point) <= len(self.task_list)

        # If all tasks have already been selected and this solution is better than the current best one, replace it
        # and return
        if len(starting_point) == len(self.task_list) and (
                not self.best_turnaround_time or accumulated_turnaround_time < self.best_turnaround_time):
            self.best_turnaround_time = accumulated_turnaround_time
            self.optimal_order = starting_point
            return

        # Branch for all tasks absent in `starting_point`
        remaining_tasks = [task for task in self.task_list if task not in starting_point]
        for task in remaining_tasks:
            task_end_time = max(passed_time, task.come_time) + task.duration
            self.recurse_tasks(starting_point + [task], task_end_time,
                               accumulated_turnaround_time + task_end_time - task.come_time)

    def select_next_task(self) -> Optional[Task]:
        # Select tasks in the optimal order. If the next task to be run is not yet waiting, return `None`.
        if self.optimal_order[0] in self.waiting_tasks:
            self.waiting_tasks.remove(self.optimal_order[0])
            return self.optimal_order.pop(0)
        return None
