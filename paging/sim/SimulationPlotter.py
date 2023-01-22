from typing import Dict, List
from matplotlib import pyplot
from .MemoryManagerGroup import MemoryManagerGroup


class SimulationPlotter:
    def __init__(self):
        self.figure = None
        self.axes = None

    def generate_plot(self, mm_groups: List[MemoryManagerGroup]):
        data_page_faults: Dict[str, Dict[str, List[int]]] = {}

        for mm_group in mm_groups:
            for mm_name, mm in mm_group.memory_managers.items():
                mm_algo, mm_size = mm_name.split('_')

                if mm_size not in data_page_faults.keys():
                    data_page_faults[mm_size] = {}

                if mm_algo not in data_page_faults[mm_size].keys():
                    data_page_faults[mm_size][mm_algo] = []

                data_page_faults[mm_size][mm_algo].append(mm.page_faults)

        self.figure, self.axes = pyplot.subplots(len(data_page_faults), sharex='col',
                                                 figsize=[6.4, 4.8 + 2 * (len(data_page_faults) - 2)],
                                                 layout='compressed')

        try:
            len(self.axes)
        except TypeError:
            self.axes = [self.axes]

        for i in range(len(self.axes)):
            memory_size = list(data_page_faults.keys())[i]
            for mm_algo, page_faults in data_page_faults[memory_size].items():
                self.axes[i].plot(page_faults, '.', label=mm_algo)
            self.axes[i].set_title('Memory size: ' + str(memory_size), fontsize='medium')
            self.axes[i].set_box_aspect(1 / 3)

        self.figure.suptitle('Page faults vs simulation number')
        self.figure.supxlabel('Simulation', fontsize='small')
        self.figure.supylabel('Page faults', fontsize='small')
        self.axes[0].legend(framealpha=0.5, fontsize='xx-small', markerscale=0.5)

    def save_plot(self, output_file: str):
        self.figure.savefig(output_file)
