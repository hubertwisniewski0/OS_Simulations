from typing import List, Optional
from copy import deepcopy
from numpy import average
from utils.Serializable import Serializable
from .Task import Task


class Scheduler(Serializable):
    """
    General task scheduler implementation
    """
    def __init__(self, task_list: List[Task]):
        """
        :param task_list: list of tasks to process
        """
        # Deep copy is required as tasks are modified themselves during simulation
        self.task_list = deepcopy(task_list)
        self.waiting_tasks: List[Task] = []
        self.complete_tasks: List[Task] = []
        self.current_task: Optional[Task] = None
        self.current_time = 0
        self.total_idle_time = 0

        # Information holders for statistical analysis
        self.task_waiting_times: List[int] = []
        self.task_turnaround_times: List[int] = []
        self.average_task_waiting_time = None
        self.average_task_turnaround_time = None

    def tick(self) -> bool:
        """
        Perform a single simulation step (advance the time by one)
        :return: whether there are any unfinished tasks left
        """
        self.detect_new_tasks()

        # If there is any task being currently executed, serve it
        if self.current_task:
            self.current_task.tick()
            if self.current_task.is_complete():
                self.complete_tasks.append(self.current_task)
                self.current_task = None

        # If there is no task being currently executed, select the next one or end the simulation
        if not self.current_task:
            if len(self.task_list) == 0 and len(self.waiting_tasks) == 0:
                self.generate_stats()
                return False
            self.current_task = self.select_next_task()
            if self.current_task:
                self.current_task.start(self.current_time)

        self.current_time += 1

        if not self.current_task:
            self.total_idle_time += 1

        return True

    def detect_new_tasks(self):
        """
        Search for tasks that already came
        """
        new_task_list: List[Task] = []

        # Split all not-waiting tasks for those which already came and those which did not
        for task in self.task_list:
            assert task.come_time >= self.current_time

            if task.come_time == self.current_time:
                self.waiting_tasks.append(task)
            else:
                new_task_list.append(task)

        self.task_list = new_task_list

    def generate_stats(self):
        """
        Generate average waiting and turnaround time statistics
        """
        self.task_waiting_times = [task.waiting_time for task in self.complete_tasks]
        self.task_turnaround_times = [task.turnaround_time for task in self.complete_tasks]
        self.average_task_waiting_time = average(self.task_waiting_times)
        self.average_task_turnaround_time = average(self.task_turnaround_times)

    def serialize(self):
        return {
            "total_time": self.current_time,
            "total_idle_time": self.total_idle_time,
            "average_task_waiting_time": self.average_task_waiting_time,
            "average_task_turnaround_time": self.average_task_turnaround_time,
            "complete_tasks": self.complete_tasks
        }

    def select_next_task(self) -> Optional[Task]:
        """
        Select the next task to be run
        :return: task or `None` if there are no waiting tasks
        """
        raise NotImplementedError()
