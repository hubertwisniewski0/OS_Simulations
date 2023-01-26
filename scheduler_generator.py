import json
from argparse import ArgumentParser
from typing import List

from sched.core.TaskBase import TaskBase
from sched.sim.SimulationDescription import SimulationDescription
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
    if args_.come_time[0] < 0:
        raise ValueError('Come time lower bound must be a non-negative integer')
    if args_.come_time[0] > args_.come_time[1]:
        raise ValueError('Come time lower bound must not be lower than the upper one')
    if args_.duration[0] < 1:
        raise ValueError('Duration lower bound must be a positive integer')
    if args_.duration[0] > args_.duration[1]:
        raise ValueError('Duration lower bound must not be lower than the upper one')


# Define and parse arguments
ap = ArgumentParser(description='Generate scheduler simulation input data',
                    epilog='NOTE: values generated using Gaussian distribution are still confined to their respective '
                           'bounds!')
ap.add_argument('output_file', type=str, help='Generated data output file')
ap.add_argument('-n', '--simulations', type=int, default=100, help='Number of separate simulations (default: 100)')
ap.add_argument('-l', '--simulation-length', type=int, default=100,
                help='Number of tasks in a single simulation (default: 100)')
ap.add_argument('-c', '--come-time', nargs=2, type=int, metavar=('MIN', 'MAX'), default=[0, 99],
                help='Task come time bounds (inclusive, default: 0 99)')
ap.add_argument('-d', '--duration', nargs=2, type=int, metavar=('MIN', 'MAX'), default=[1, 20],
                help='Task duration bounds (inclusive, default: 1 20)')
ap.add_argument('-f', '--gaussian-come-time', nargs=2, type=float, metavar=('MEAN', 'STDDEV'),
                help='Use normal (Gaussian) distribution to generate task come time (default: use uniform distribution)'
                )
ap.add_argument('-g', '--gaussian-duration', nargs=2, type=float, metavar=('MEAN', 'STDDEV'),
                help='Use normal (Gaussian) distribution to generate task duration (default: use uniform distribution)'
                )
ap.add_argument('-s', '--seed', help='Seed for the random number generator (default: use the current system time)')
args = ap.parse_args()

check_args(args)

rng = ExtendedRandom(args.seed)

simulations: List[SimulationDescription] = []

# Create simulation input data according to provided arguments and/or their values
for i in range(args.simulations):
    desc = SimulationDescription()
    desc.task_list = []

    for j in range(args.simulation_length):
        come_time = rng.bounded_int_gaussian(args.come_time[0], args.come_time[1], args.gaussian_come_time[0],
                                             args.gaussian_come_time[1]) if args.gaussian_come_time else rng.randint(
            args.come_time[0], args.come_time[1])
        duration = rng.bounded_int_gaussian(args.duration[0], args.duration[1], args.gaussian_duration[0],
                                            args.gaussian_duration[1]) if args.gaussian_duration else rng.randint(
            args.duration[0], args.duration[1])

        desc.task_list.append(TaskBase(come_time, duration))

    # Generate a random seed for lottery algorithm for predictability
    desc.lottery_seed = rng.getrandbits(64)
    simulations.append(desc)

# Save data
with open(args.output_file, 'wt') as f:
    json.dump(simulations, f, indent=4, cls=Encoder)
