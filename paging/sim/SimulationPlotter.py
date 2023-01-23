from typing import Dict, List
from matplotlib import pyplot
from .MemoryManagerGroup import MemoryManagerGroup


class SimulationPlotter:
    """
    Creates a plot using `matplotlib`
    """
    def __init__(self):
        self.figure = None
        self.axes = None

    @staticmethod
    def extract_data(mm_groups: List[MemoryManagerGroup]) -> Dict[str, Dict[str, List[int]]]:
        """
        Extract simulation results
        :param mm_groups: list of memory manager groups to extract data from
        :return: plottable data:
            Dict[
                memory_size: str,
                Dict[
                    algorithm_name: str,
                    List[
                        page_faults: int,
                        ...
                    ]
                ]
            ]
        """
        data_page_faults: Dict[str, Dict[str, List[int]]] = {}

        for mm_group in mm_groups:
            for mm_name, mm in mm_group.memory_managers.items():
                mm_algo, mm_size = mm_name.split('_')

                if mm_size not in data_page_faults.keys():
                    data_page_faults[mm_size] = {}

                if mm_algo not in data_page_faults[mm_size].keys():
                    data_page_faults[mm_size][mm_algo] = []

                data_page_faults[mm_size][mm_algo].append(mm.page_faults)

        return data_page_faults

    def generate_plot(self, mm_groups: List[MemoryManagerGroup]):
        """
        Generate plot based on complete simulations
        :param mm_groups: list of memory manager groups to get data from
        """
        data_page_faults = self.extract_data(mm_groups)

        # Create figure and axes with geometry based on the number of simulated memory sizes
        self.figure, self.axes = pyplot.subplots(len(data_page_faults), sharex='col',
                                                 figsize=[6.4, 4.8 + 2 * (len(data_page_faults) - 2)],
                                                 layout='compressed')

        # If there is only one memory size (self.axes has no length), make it a single-element list to allow iteration
        try:
            len(self.axes)
        except TypeError:
            self.axes = [self.axes]

        # Plot data for each memory size for each algorithm as dots. Set title and aspect ratio for each ax.
        for i in range(len(self.axes)):
            memory_size = list(data_page_faults.keys())[i]
            for mm_algo, page_faults in data_page_faults[memory_size].items():
                self.axes[i].plot(page_faults, '.', label=mm_algo)
            self.axes[i].set_title('Memory size: ' + memory_size, fontsize='medium')
            self.axes[i].set_box_aspect(1 / 3)

        # Title and axis' labels are only needed once - globally
        self.figure.suptitle('Page faults vs simulation number')
        self.figure.supxlabel('Simulation', fontsize='small')
        self.figure.supylabel('Page faults', fontsize='small')

        # Legend is only needed on one axes - all data subsets are plotted in the same order and as a result they
        # have the same color
        self.axes[0].legend(framealpha=0.5, fontsize='xx-small', markerscale=0.5)

    def save_plot(self, output_file: str):
        """
        Save the generated plot to file
        :param output_file: name of the file to save the plot to
        """
        self.figure.savefig(output_file)
