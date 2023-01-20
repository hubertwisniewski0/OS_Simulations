import json
from random import Random
from typing import List
from sched.core.TaskBase import TaskBase
from sched.sim.SimulationDescription import SimulationDescription
from utils.Encoder import Encoder

simulations: List[SimulationDescription] = []
rng = Random()

for i in range(100):
    desc = SimulationDescription()
    desc.task_list = [TaskBase(rng.randint(0, 99), rng.randint(1, 20)) for j in range(100)]
    desc.lottery_seed = rng.getrandbits(64)
    simulations.append(desc)

with open('gen_out.json', 'wt') as f:
    json.dump(simulations, f, indent=4, cls=Encoder)
