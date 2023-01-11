from .Task import Task


class TaskFactory:
    def __init__(self):
        self.created_tasks = 0

    def create_task(self, come_time: int, duration: int) -> Task:
        new_task = Task(self.created_tasks, come_time, duration)
        self.created_tasks += 1
        return new_task
