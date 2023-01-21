import json
from random import Random
from typing import List
from paging.sim.SimulationDescription import SimulationDescription
from utils.Encoder import Encoder

simulations: List[SimulationDescription] = []
rng = Random()

for i in range(100):
    desc = SimulationDescription()
    desc.access_list = [rng.randint(0, 19) for j in range(100)]
    desc.memory_sizes = [3, 5, 7]
    simulations.append(desc)

with open('gen_out.json', 'wt') as f:
    json.dump(simulations, f, indent=4, cls=Encoder)
