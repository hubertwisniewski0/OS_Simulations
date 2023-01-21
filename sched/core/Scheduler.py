from typing import List, Optional
from copy import deepcopy
from numpy import average
from utils.Serializable import Serializable
from .Task import Task


class Scheduler(Serializable):
    def __init__(self, task_list: List[Task]):
        self.task_list = deepcopy(task_list)
        self.waiting_tasks: List[Task] = []
        self.complete_tasks: List[Task] = []
        self.current_task: Optional[Task] = None
        self.current_time = 0
        self.total_idle_time = 0
        self.task_waiting_times: List[int] = []
        self.task_turnaround_times: List[int] = []
        self.average_task_waiting_time = None
        self.average_task_turnaround_time = None

    def tick(self) -> bool:
        self.detect_new_tasks()

        if self.current_task:
            self.current_task.tick()
            if self.current_task.is_complete():
                self.complete_tasks.append(self.current_task)
                self.current_task = None

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
        new_waiting_tasks: List[Task] = []

        for task in self.task_list:
            assert task.come_time >= self.current_time

            if task.come_time == self.current_time:
                new_waiting_tasks.append(task)

        for task in new_waiting_tasks:
            self.task_list.remove(task)

        self.waiting_tasks += new_waiting_tasks

    def generate_stats(self):
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
        raise NotImplementedError()
