# CPU Scheduling Simulator

A comprehensive Python implementation of four major CPU scheduling algorithms with detailed explanations and performance metrics.

## Overview

This project implements and demonstrates four fundamental CPU scheduling algorithms used in operating systems:

1. **FCFS (First Come First Serve)** - Non-preemptive, processes execute in arrival order
2. **SJF (Shortest Job First)** - Preemptive, shortest remaining burst time first
3. **Priority Scheduling** - Preemptive, highest priority processes first
4. **Round Robin** - Preemptive, fixed time quantum for each process

## Features

- **Interactive Menu System**: Easy-to-use command-line interface
- **Detailed Output**: Formatted tables showing all process metrics
- **Gantt Chart Sequences**: Visual representation of process execution order
- **Performance Metrics**: Average waiting time and turnaround time calculations
- **Comprehensive Comments**: Well-documented code explaining each algorithm
- **Error Handling**: Input validation and user-friendly error messages

## Installation

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the simulator**:
   ```bash
   python main.py
   ```

## How to Use

1. **Start the program**: Run `python main.py`
2. **Choose algorithm**: Select from the menu (1-4)
3. **Enter process details**: For each process, provide:
   - Process ID (unique identifier)
   - Arrival Time (when process arrives)
   - Burst Time (execution time needed)
   - Priority (for Priority Scheduling)
   - Time Quantum (for Round Robin)
4. **View results**: See formatted tables and performance metrics
5. **Run another algorithm**: Choose to compare different algorithms

## Algorithm Details

### 1. FCFS (First Come First Serve)
- **Type**: Non-preemptive
- **Selection**: First process to arrive gets CPU first
- **Advantages**: Simple, no starvation
- **Disadvantages**: Poor performance with varying burst times

### 2. SJF (Shortest Job First)
- **Type**: Preemptive
- **Selection**: Process with shortest remaining burst time
- **Advantages**: Minimizes average waiting time
- **Disadvantages**: Can cause starvation, requires burst time knowledge

### 3. Priority Scheduling
- **Type**: Preemptive
- **Selection**: Process with highest priority number
- **Advantages**: Allows process prioritization
- **Disadvantages**: Can cause starvation for low priority processes

### 4. Round Robin
- **Type**: Preemptive
- **Selection**: Each process gets fixed time quantum
- **Advantages**: Fair scheduling, no starvation
- **Disadvantages**: Performance depends on time quantum size

## Performance Metrics

The simulator calculates and displays:

- **Completion Time**: When each process finishes
- **Turnaround Time**: Total time from arrival to completion
- **Waiting Time**: Time spent waiting in ready queue
- **Average Metrics**: Overall system performance

## File Structure

```
CA_Progress/
├── main.py                 # Main program and menu system
├── FCFS.py                # First Come First Serve implementation
├── SJF.py                 # Shortest Job First implementation
├── PriorityScheduling.py  # Priority scheduling implementation
├── RoundRobin.py          # Round Robin implementation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Example Usage

```
===== CPU SCHEDULING SIMULATOR =====

WHICH ALGORITHM DO YOU WANT TO RUN?

1. PRESS 1 FOR FCFS ALGORITHM (First Come First Serve)
2. PRESS 2 FOR SJF ALGORITHM (Shortest Job First)
3. PRESS 3 FOR Priority ALGORITHM (Priority-based Scheduling)
4. PRESS 4 FOR Round-Robin ALGORITHM (Time Quantum Scheduling)

ENTER A NUMBER: 1

How many Processes do you want to run in the system? 3

=== Running FCFS (First Come First Serve) Algorithm ===

Enter details for 3 processes:
Note: Lower arrival time means process arrives earlier
Enter Process ID: 1
Enter Arrival Time for Process 1: 0
Enter Burst Time for Process 1: 5
...
```

## Understanding the Output

### Table Columns
- **P ID**: Process ID
- **AT**: Arrival Time
- **BT/Rem_BT**: Burst Time / Remaining Burst Time
- **CT**: Completion Time
- **TAT**: Turnaround Time
- **WT**: Waiting Time
- **Priority**: Priority Level (Priority Scheduling only)

### Gantt Chart
Shows the sequence of process execution over time, useful for visualizing how the CPU is allocated.

## Algorithm Comparison

| Algorithm | Preemptive | Starvation | Complexity | Best For |
|-----------|------------|------------|------------|----------|
| FCFS | No | No | Low | Simple systems |
| SJF | Yes | Yes | Medium | Batch processing |
| Priority | Yes | Yes | Medium | Real-time systems |
| Round Robin | Yes | No | Medium | Time-sharing |

## Contributing

Feel free to:
- Report bugs or issues
- Suggest improvements
- Add new scheduling algorithms
- Enhance the documentation

## Educational Purpose

This project is designed for educational purposes to help understand:
- CPU scheduling concepts
- Algorithm implementation
- Performance analysis
- Operating system principles

## Requirements

- Python 3.6 or higher
- tabulate library (for formatted output)

## License

This project is open source and available for educational use. 