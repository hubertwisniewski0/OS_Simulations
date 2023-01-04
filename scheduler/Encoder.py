from typing import Union, Dict
from json import JSONEncoder
from scheduler.Scheduler import Scheduler
from scheduler.Task import Task


class Encoder(JSONEncoder):
    def default(self, o: Union[Scheduler, Task]) -> Dict:
        if isinstance(o, Scheduler):
            return {"complete_tasks": o.complete_tasks,
                    "total_time": o.current_time,
                    "total_idle_time": o.total_idle_time}
        elif isinstance(o, Task):
            return {"task_id": o.task_id,
                    "come_time": o.come_time,
                    "duration": o.duration,
                    "wait_time": o.get_wait_time()}
        else:
            return super().default(o)
