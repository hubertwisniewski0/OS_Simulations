from enum import Enum, auto

from .TaskBase import TaskBase


class TaskStatus(Enum):
    """
    Task status enumeration (exact values are irrelevant and should not be relied upon)
    """
    Waiting = auto()
    Running = auto()
    Complete = auto()


class Task(TaskBase):
    """
    Task class
    """

    def __init__(self, task_id: int, come_time: int, duration: int):
        """
        :param task_id: unique task ID
        :param come_time: time when the task becomes available to be run
        :param duration: time that the task takes to run
        """
        super().__init__(come_time, duration)

        assert task_id >= 0

        self.task_id = task_id
        self.status = TaskStatus.Waiting
        self.start_time = None
        self.total_runtime = 0
        self.waiting_time = None
        self.turnaround_time = None

    def start(self, start_time: int):
        """
        Start the task
        :param start_time: time when the task has been started
        """
        assert self.status == TaskStatus.Waiting

        self.status = TaskStatus.Running
        self.start_time = start_time
        self.waiting_time = start_time - self.come_time

    def tick(self):
        """
        Perform a single time step (update the task's runtime and check for completeness)
        """
        assert self.status == TaskStatus.Running
        assert self.total_runtime < self.duration

        self.total_runtime += 1
        if self.total_runtime == self.duration:
            self.status = TaskStatus.Complete
            self.turnaround_time = self.waiting_time + self.duration

    def is_complete(self) -> bool:
        """
        Check whether the task is complete
        """
        return self.status == TaskStatus.Complete

    def serialize(self):
        return {
            "task_id": self.task_id,
            "come_time": self.come_time,
            "duration": self.duration,
            "waiting_time": self.waiting_time,
            "turnaround_time": self.turnaround_time
        }
