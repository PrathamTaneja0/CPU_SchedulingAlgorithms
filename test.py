import csv
import sys
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive display
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
from io import StringIO
from FCFS import FCFS
from SJF import SJF
from Priority import Priority
from RR import RoundRobin
import time

def load_processes_from_csv(filename):
    processes = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pid = int(row['PID'])
            arrival = int(row['Arrival'])
            burst = int(row['Burst'])
            priority = int(row['Priority']) if 'Priority' in row and row['Priority'] != '' else None
            if priority is not None:
                processes.append([pid, arrival, burst, priority])
            else:
                processes.append([pid, arrival, burst])
    return processes

def run_fcfs(processes):
    print("\n=== FCFS Test ===")
    fcfs = FCFS()
    # FCFS expects [PID, Arrival, Burst] - create a copy
    proc = [p[:3].copy() for p in processes]
    fcfs.processData(proc)
    plt.show()

def run_sjf(processes):
    print("\n=== SJF Test ===")
    sjf = SJF()
    # SJF expects [PID, Arrival, Burst] - create a copy
    proc = [p[:3].copy() for p in processes]
    sjf.processData(proc)
    plt.show()

def run_priority(processes):
    print("\n=== Priority Test ===")
    priority = Priority()
    # Priority expects [PID, Arrival, Burst, Priority] - create a copy
    proc = [p.copy() for p in processes]
    priority.processData(proc)
    plt.show()

def run_rr(processes, time_quantum=2):
    print(f"\n=== Round Robin Test (Time Quantum = {time_quantum}) ===")
    rr = RoundRobin()
    # RR expects [PID, Arrival, Burst] or [PID, Arrival, Burst, Priority] - create a copy
    proc = [p.copy() for p in processes]
    # Simulate input for time quantum
    old_stdin = sys.stdin
    sys.stdin = StringIO(f"{time_quantum}\n")
    try:
        rr.processData(proc)
        plt.show()
    finally:
        sys.stdin = old_stdin

def main():
    processes = load_processes_from_csv('test.csv')
    run_fcfs(processes)
    run_sjf(processes)
    run_priority(processes)
    run_rr(processes, time_quantum=2)

if __name__ == "__main__":
    main() 