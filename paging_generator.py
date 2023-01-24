import json
from argparse import ArgumentParser
from typing import List

from paging.sim.SimulationDescription import SimulationDescription
from utils.Encoder import Encoder
from utils.ExtendedRandom import ExtendedRandom


def check_args(args_):
    """
    Check arguments' correctness
    :param args_: argparse arguments namespace
    """
    if args_.simulations < 1:
        raise ValueError('Number of simulations must be a positive integer')
    if args_.simulation_length < 1:
        raise ValueError('Simulation length must be a positive integer')
    if args_.page_access[0] < 0:
        raise ValueError('Page access lower bound must be a non-negative integer')
    if args_.page_access[0] > args_.page_access[1]:
        raise ValueError('Page access lower bound must not be lower than the upper one')
    if not all(map(lambda x: x > 0, args_.memory_sizes)):
        raise ValueError('All memory sizes must be positive integers')


# Define and parse arguments
ap = ArgumentParser(description='Generate paging simulation input data',
                    epilog='NOTE: values generated using Gaussian distribution are still confined to their respective '
                           'bounds!')
ap.add_argument('output_file', type=str, help='Generated data output file')
ap.add_argument('-n', '--simulations', type=int, default=100, help='Number of separate simulations (default: 100)')
ap.add_argument('-l', '--simulation-length', type=int, default=100,
                help='Number of page accesses in a single simulation (default: 100)')
ap.add_argument('-p', '--page-access', nargs=2, type=int, metavar=('MIN', 'MAX'), default=[0, 19],
                help='Accessed page number bounds (inclusive, default: 0 19)')
ap.add_argument('-g', '--gaussian-page-access', nargs=2, type=float, metavar=('MEAN', 'STDDEV'),
                help='Use normal (Gaussian) distribution to generate accessed page number (default: use uniform '
                     'distribution)')
ap.add_argument('-m', '--memory-sizes', nargs='+', type=int, metavar='SIZE', default=[3, 5, 7],
                help='Memory sizes to use for simulation (default: 3 5 7)')
ap.add_argument('-s', '--seed', help='Seed for the random number generator (default: use the current system time)')
args = ap.parse_args()

check_args(args)

rng = ExtendedRandom(args.seed)

simulations: List[SimulationDescription] = []

# Create simulation input data according to provided arguments and/or their values
for i in range(args.simulations):
    desc = SimulationDescription()
    desc.access_list = [rng.bounded_int_gaussian(args.page_access[0], args.page_access[1], args.gaussian_page_access[0],
                                                 args.gaussian_page_access[1]) if args.gaussian_page_access else
                        rng.randint(args.page_access[0], args.page_access[1]) for j in range(args.simulation_length)]
    desc.memory_sizes = args.memory_sizes
    simulations.append(desc)

# Save data
with open(args.output_file, 'wt') as f:
    json.dump(simulations, f, indent=4, cls=Encoder)
