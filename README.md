# Operating Systems simulations

This project contains task scheduler and page replacement simulations created for an assignment on Operating Systems
laboratory. The following algorithms are currently implemented:

- Scheduling (without preemption):
    - First Come First Serve
    - Shortest Job First
    - Lottery algorithm
    - Non-causal optimal algorithm*
- Page replacement:
    - First In First Out (unmodified)
    - Least Frequently Used
    - Most Frequently Used
    - Non-causal optimal algorithm

*pseudo-brute-force implementation, very high computational complexity

Most notable features:

- Data input and output using JSON files
- Input data validation against JSON schemas
- Concurrent simulations (multiprocessing)
- Output data plotting using *Matplotlib*
- Input data generators with many options

## Requirements

The following software is required to run scripts contained in this project:

- Python3 interpreter (recommended version: 3.9.2)
- modules listed in `requirements.txt`

## Setup

1. Create a virtual environment (optional but recommended):
    ```
    python3 -m venv venv
    . venv/bin/activate
    ```

2. Install the required packages:
    ```
    pip3 install -r requirements.txt
    ```

## Usage

All scripts take arguments that can be displayed using `--help`, for example:

```
python3 scheduler_simulation.py --help
```

## Examples

- Generate scheduler input data with default parameters and save it to `sched_in.json`:
  ```
  python3 scheduler_generator.py sched_in.json
  ```

- Perform scheduler simulation based on the generated data from `sched_in.json` and save raw output data and plot
to `sched_out.json` and `sched_out.svg` respectively:
  ```
  python3 scheduler_simulation.py sched_in.json sched_out.json sched_out.svg
  ```
