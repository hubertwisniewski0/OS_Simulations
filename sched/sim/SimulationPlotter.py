from typing import Dict, List
from matplotlib import pyplot
from .SchedulerGroup import SchedulerGroup


class SimulationPlotter:
    def __init__(self):
        self.figure = None
        self.axes = None

    def generate_plot(self, scheduler_groups: List[SchedulerGroup]):
        self.figure, self.axes = pyplot.subplots()

        data_turnaround_time: Dict[str, List[float]] = {}
        data_waiting_time: Dict[str, List[float]] = {}

        for scheduler_group in scheduler_groups:
            for scheduler in scheduler_group.schedulers.keys():
                if scheduler not in data_turnaround_time.keys():
                    data_turnaround_time[scheduler] = []
                if scheduler not in data_waiting_time.keys():
                    data_waiting_time[scheduler] = []

                data_turnaround_time[scheduler].append(
                    scheduler_group.schedulers[scheduler].get_average_task_turnaround_time())
                data_waiting_time[scheduler].append(
                    scheduler_group.schedulers[scheduler].get_average_task_waiting_time())

        for scheduler in data_turnaround_time.keys():
            self.axes.plot(data_turnaround_time[scheduler], '.', label=scheduler + ' (turnaround)')

        for scheduler in data_waiting_time.keys():
            self.axes.plot(data_waiting_time[scheduler], '+', label=scheduler + ' (waiting)')

        self.axes.set_title('Average turnaround/waiting time vs simulation number')
        self.axes.set_xlabel('Simulation')
        self.axes.set_ylabel('Average turnaround/waiting time [cycles]')
        self.axes.legend(framealpha=0.5, fontsize='xx-small', markerscale=0.5)

    def save_plot(self, output_file: str):
        self.figure.savefig(output_file)
