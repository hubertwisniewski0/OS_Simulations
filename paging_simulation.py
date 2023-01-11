import json
from argparse import ArgumentParser
from paging.sim.MemoryManagerSimulation import MemoryManagerSimulation
from utils.Encoder import Encoder

ap = ArgumentParser()
ap.add_argument('input_file', help='Data input file')
args = ap.parse_args()

simulation = MemoryManagerSimulation()
simulation.read_data(args.input_file)
simulation.simulate()

print(json.dumps(simulation, indent=4, cls=Encoder))
