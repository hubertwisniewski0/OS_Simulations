from .Task import Task


class TaskFactory:
    """
    Creates tasks with unique IDs
    """

    def __init__(self):
        self.created_tasks = 0

    def create_task(self, come_time: int, duration: int) -> Task:
        """
        Create a new task with unique ID
        :param come_time: time when the task becomes available to be run
        :param duration: time that the task takes to run
        :return: a new task
        """
        new_task = Task(self.created_tasks, come_time, duration)
        self.created_tasks += 1
        return new_task
