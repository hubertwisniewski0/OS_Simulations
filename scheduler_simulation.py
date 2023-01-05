from copy import deepcopy
from typing import List, Dict
import json
from argparse import ArgumentParser
from scheduler.SchedulerFCFS import SchedulerFCFS
from scheduler.SchedulerSJF import SchedulerSJF
from scheduler.Task import Task
from utils.Encoder import Encoder

ap = ArgumentParser()
ap.add_argument('input_file', help='Data input file')
args = ap.parse_args()

with open(args.input_file, 'rt') as f:
    input_data: List[Dict] = json.load(f)

tasks: List[Task] = []
task_id_counter = 0

for input_task in input_data:
    tasks.append(Task(task_id_counter, input_task['come_time'], input_task['duration']))
    task_id_counter += 1

sched_fcfs = SchedulerFCFS(deepcopy(tasks))

while sched_fcfs.tick():
    pass

sched_sjf = SchedulerSJF(deepcopy(tasks))

while sched_sjf.tick():
    pass

print(json.dumps(
    {"FCFS": sched_fcfs,
     "SJF": sched_sjf}
    , cls=Encoder, indent=4))
