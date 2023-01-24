import json
from argparse import ArgumentParser

from paging.sim.MemoryManagerSimulation import MemoryManagerSimulation
from utils.Encoder import Encoder


def check_args(args_):
    """
    Check arguments' correctness
    :param args_: argparse arguments namespace
    """
    if args_.jobs is not None and args_.jobs < 1:
        raise ValueError('Maximum number of workers must be a positive integer')


# Define and parse arguments
ap = ArgumentParser(description='Page replacement simulation')
ap.add_argument('input_file', help='Input data file')
ap.add_argument('output_file', help='Raw output data file')
ap.add_argument('plot_output_file', help='Plot output file')
ap.add_argument('-j', '--jobs', type=int,
                help='Maximum number of concurrent simulations (default: determined automatically, see the '
                     'documentation of `concurrent.futures` module)')
args = ap.parse_args()

check_args(args)

# Perform simulation
simulation = MemoryManagerSimulation(args.jobs)
simulation.read_data(args.input_file)
simulation.simulate()
simulation.generate_stats()
simulation.create_plot(args.plot_output_file)

# Dump simulation data
with open(args.output_file, 'wt') as f:
    json.dump(simulation, f, indent=4, cls=Encoder)
