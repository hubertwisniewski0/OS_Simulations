from typing import Dict, List, Tuple
from matplotlib import pyplot
from .SchedulerGroup import SchedulerGroup


class SimulationPlotter:
    def __init__(self):
        self.figure = None
        self.axes = None

    @staticmethod
    def extract_data(scheduler_groups: List[SchedulerGroup]) -> Tuple[Dict[str, List[float]], Dict[str, List[float]]]:
        data_turnaround_time: Dict[str, List[float]] = {}
        data_waiting_time: Dict[str, List[float]] = {}

        for scheduler_group in scheduler_groups:
            for scheduler_algo, scheduler in scheduler_group.schedulers.items():
                if scheduler_algo not in data_turnaround_time.keys():
                    data_turnaround_time[scheduler_algo] = []
                if scheduler_algo not in data_waiting_time.keys():
                    data_waiting_time[scheduler_algo] = []

                data_turnaround_time[scheduler_algo].append(scheduler.average_task_turnaround_time)
                data_waiting_time[scheduler_algo].append(scheduler.average_task_waiting_time)

        return data_turnaround_time, data_waiting_time

    def generate_plot(self, scheduler_groups: List[SchedulerGroup]):
        data_turnaround_time, data_waiting_time = self.extract_data(scheduler_groups)

        self.figure, self.axes = pyplot.subplots(2, sharex='col')

        data = [data_turnaround_time, data_waiting_time]
        for i in range(2):
            for scheduler_algo, scheduler_stats in data[i].items():
                self.axes[i].plot(scheduler_stats, '.', label=scheduler_algo)

        self.axes[0].set_title('Turnaround time', fontsize='medium')
        self.axes[1].set_title('Waiting time', fontsize='medium')

        self.figure.suptitle('Average turnaround/waiting time vs simulation number')
        self.figure.supxlabel('Simulation', fontsize='small')
        self.figure.supylabel('Average turnaround/waiting time [cycles]', fontsize='small')
        self.axes[0].legend(framealpha=0.5, fontsize='xx-small', markerscale=0.5)

    def save_plot(self, output_file: str):
        self.figure.savefig(output_file)
