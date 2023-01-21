import json
from argparse import ArgumentParser
from sched.sim.SchedulerSimulation import SchedulerSimulation
from utils.Encoder import Encoder

ap = ArgumentParser(description='Task scheduler simulation')
ap.add_argument('input_file', help='Input data file')
ap.add_argument('output_file', help='Raw output data file')
ap.add_argument('plot_output_file', help='Plot output file')
ap.add_argument('-j', '--jobs', type=int,
                help='Maximum number of concurrent simulations (default: determined automatically, see the '
                     'documentation of `concurrent.futures` module)')
ap.add_argument('-o', '--optimal', action='store_true',
                help='Enable optimal algorithm (caution: very high computational complexity!)')
args = ap.parse_args()

simulation = SchedulerSimulation(args.jobs, args.optimal)
simulation.read_data(args.input_file)
simulation.simulate()
simulation.create_plot(args.plot_output_file)

with open(args.output_file, 'wt') as f:
    json.dump(simulation, f, indent=4, cls=Encoder)
