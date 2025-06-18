# CPU Scheduling Simulator

A Python project implementing and visualizing four classic CPU scheduling algorithms: FCFS, SJF, Priority, and Round Robin. Supports both manual and CSV input, and generates Gantt charts for each algorithm.

## Features
- **Algorithms:** FCFS, SJF (preemptive), Priority (preemptive), Round Robin
- **Input:** Manual entry or CSV file (`processes.csv`)
- **Output:** Tabulated results and Gantt chart visualization (using matplotlib)
- **Well-documented code**
- **Extensible and educational**

## Requirements
- Python 3.6+
- [tabulate](https://pypi.org/project/tabulate/)
- [matplotlib](https://pypi.org/project/matplotlib/)

Install dependencies:
```bash
pip install -r requirements.txt
```

## File Structure
```
CA_Progress/
├── FCFS.py         # First-Come, First-Served logic
├── SJF.py          # Shortest-Job-First logic
├── Priority.py     # Priority Scheduling logic
├── RR.py           # Round Robin logic (uses collections.deque)
├── main.py         # Main entry point, handles input and runs algorithms
├── processes.csv   # Example input file (CSV format)
├── requirements.txt
└── README.md
```

## Usage
1. **Run the simulator:**
   ```bash
   python main.py
   ```
2. **Choose an algorithm** (FCFS, SJF, Priority, RR)
3. **Choose input mode:**
   - Manual entry (enter process details one by one)
   - CSV file (`processes.csv`)
4. **View results:**
   - Tabulated process metrics (Completion, Turnaround, Waiting Time)
   - Gantt chart visualization (matplotlib window)

## Example `processes.csv`
```
PID,Arrival,Burst,Priority
1,0,5,2
2,2,3,1
3,4,1,3
```
- For FCFS/SJF/RR, Priority column is ignored.
- For Priority scheduling, Priority column is used.

## Module Overview

### main.py
- Loads process data (manual or CSV)
- Lets user select algorithm
- Runs selected algorithm and displays results

### FCFS.py
- Implements First-Come, First-Served logic
- Outputs table and Gantt chart

### SJF.py
- Implements Preemptive Shortest-Job-First logic
- Outputs table and Gantt chart

### Priority.py
- Implements Preemptive Priority Scheduling logic
- Outputs table and Gantt chart

### RR.py
- Implements Round Robin logic (uses `collections.deque` for ready queue)
- Prompts for time quantum
- Outputs table and Gantt chart

## Libraries Used
- **tabulate:** For clean table output
- **matplotlib:** For Gantt chart visualization
- **csv:** For reading CSV input
- **collections.deque:** For efficient queue in Round Robin

## Extending/Modifying
- Add more columns to `processes.csv` as needed
- Add new scheduling algorithms as separate modules
- Adjust Gantt chart code for more advanced visualization

## Educational Notes
- Each algorithm is implemented in a modular, readable way
- Gantt charts help visualize scheduling behavior
- Code is commented and structured for learning and extension

## License
Open source, for educational use. 