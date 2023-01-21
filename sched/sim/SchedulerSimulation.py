import json
from typing import List, Dict
from numpy import average
from concurrent.futures import ProcessPoolExecutor, Future
from .SchedulerGroup import SchedulerGroup
from .SimulationDescription import SimulationDescription
from .SimulationPlotter import SimulationPlotter
from ..core.TaskFactory import TaskFactory
from utils.Serializable import Serializable


class SchedulerSimulation(Serializable):
    def __init__(self, jobs: int, enable_optimal: bool):
        self.scheduler_groups: List[SchedulerGroup] = []
        self.simulations: List[SimulationDescription] = []
        self.jobs = jobs
        self.enable_optimal = enable_optimal
        self.average_waiting_times: Dict[str, float] = {}
        self.average_turnaround_times: Dict[str, float] = {}

    def read_data(self, input_file_name: str):
        with open(input_file_name, 'rt') as f:
            input_data = json.load(f)

        for item in input_data:
            desc = SimulationDescription()
            desc.lottery_seed = item["lottery_seed"]

            task_factory = TaskFactory()
            desc.task_list = [task_factory.create_task(task["come_time"], task["duration"]) for task in
                              item["task_list"]]

            self.simulations.append(desc)

    def simulate(self):
        futures: List[Future] = []
        with ProcessPoolExecutor(max_workers=self.jobs) as executor:
            for simulation in self.simulations:
                sched_group = SchedulerGroup(simulation, self.enable_optimal)
                self.scheduler_groups.append(sched_group)
                futures.append(executor.submit(sched_group.simulate))

        for i in range(len(futures)):
            self.scheduler_groups[i] = futures[i].result()

        self.generate_stats()

    def create_plot(self, output_file: str):
        plotter = SimulationPlotter()
        plotter.generate_plot(self.scheduler_groups)
        plotter.save_plot(output_file)

    def generate_stats(self):
        waiting_times: Dict[str, List[int]] = {}
        turnaround_times: Dict[str, List[int]] = {}

        for sched_group in self.scheduler_groups:
            for sched_name, sched in sched_group.schedulers.items():
                if sched_name not in waiting_times.keys():
                    waiting_times[sched_name] = []
                if sched_name not in turnaround_times.keys():
                    turnaround_times[sched_name] = []

                waiting_times[sched_name] += sched.task_waiting_times
                turnaround_times[sched_name] += sched.task_turnaround_times

        for sched_name, waiting_times_list in waiting_times.items():
            self.average_waiting_times[sched_name] = average(waiting_times_list)

        for sched_name, turnaround_times_list in turnaround_times.items():
            self.average_turnaround_times[sched_name] = average(turnaround_times_list)

    def serialize(self):
        return {
            "average_waiting_times": self.average_waiting_times,
            "average_turnaround_times": self.average_turnaround_times,
            "scheduler_groups": self.scheduler_groups
        }
