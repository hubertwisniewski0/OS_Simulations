from enum import Enum, auto
from utils.Serializable import Serializable


class TaskStatus(Enum):
    Waiting = auto()
    Running = auto()
    Complete = auto()


class Task(Serializable):
    def __init__(self, task_id: int, come_time: int, duration: int):
        assert task_id >= 0
        assert come_time >= 0
        assert duration > 0

        self.task_id = task_id
        self.come_time = come_time
        self.duration = duration
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

    def get_wait_time(self) -> int:
        assert self.status != TaskStatus.Waiting
        return self.start_time - self.come_time

    def serialize(self):
        return {
            "task_id": self.task_id,
            "come_time": self.come_time,
            "duration": self.duration,
            "wait_time": self.get_wait_time()
        }
