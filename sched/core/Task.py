from enum import Enum, auto
from .TaskBase import TaskBase


class TaskStatus(Enum):
    Waiting = auto()
    Running = auto()
    Complete = auto()


class Task(TaskBase):
    def __init__(self, task_id: int, come_time: int, duration: int):
        super().__init__(come_time, duration)

        assert task_id >= 0

        self.task_id = task_id
        self.status = TaskStatus.Waiting
        self.start_time = None
        self.total_runtime = 0

    def start(self, start_time: int):
        assert self.status == TaskStatus.Waiting

        self.status = TaskStatus.Running
        self.start_time = start_time

    def tick(self):
        assert self.status == TaskStatus.Running
        assert self.total_runtime < self.duration

        self.total_runtime += 1
        if self.total_runtime == self.duration:
            self.status = TaskStatus.Complete

    def is_complete(self) -> bool:
        return self.status == TaskStatus.Complete

    def get_waiting_time(self) -> int:
        assert self.status != TaskStatus.Waiting
        return self.start_time - self.come_time

    def get_turnaround_time(self) -> int:
        return self.get_waiting_time() + self.duration

    def serialize(self):
        return {
            "task_id": self.task_id,
            "come_time": self.come_time,
            "duration": self.duration,
            "waiting_time": self.get_waiting_time(),
            "turnaround_time": self.get_turnaround_time()
        }