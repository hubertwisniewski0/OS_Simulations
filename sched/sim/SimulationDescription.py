from typing import Optional, List
from ..core.Task import Task


class SimulationDescription:
    lottery_seed: Optional[int]
    task_list: List[Task]
