import sys
from FCFS import FCFS
from SJF import SJF
from Priority import Priority
from RR import RoundRobin
import csv
import matplotlib.pyplot as plt

# Helper to load processes from CSV
def load_processes_from_csv(filename, need_priority=False):
    processes = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # All values as int, Priority is optional
            pid = int(row['PID'])
            arrival = int(row['Arrival'])
            burst = int(row['Burst'])
            if need_priority:
                priority = int(row['Priority']) if 'Priority' in row and row['Priority'] != '' else 0
                processes.append([pid, arrival, burst, priority])
            else:
                processes.append([pid, arrival, burst])
    return processes

def get_manual_input(need_priority=False):
    n = int(input("How many processes? "))
    processes = []
    for i in range(n):
        pid = int(input("Enter Process ID: "))
        arrival = int(input(f"Enter Arrival Time for Process {pid}: "))
        burst = int(input(f"Enter Burst Time for Process {pid}: "))
        if need_priority:
            priority = int(input(f"Enter Priority for Process {pid}: "))
            processes.append([pid, arrival, burst, priority])
        else:
            processes.append([pid, arrival, burst])
    return processes

def main():
    print("                                    ===== CPU SCHEDULING SIMULATOR =====")
    print("")
    print('-'*125)
    print("WHICH ALGORITHM DO YOU WANT TO RUN?")
    print("")
    print("1. PRESS 1 FOR FCFS ALGORITHM (First Come First Serve)")
    print("2. PRESS 2 FOR SJF ALGORITHM (Shortest Job First)")
    print("3. PRESS 3 FOR Priority ALGORITHM (Priority-based Scheduling)")
    print("4. PRESS 4 FOR Round-Robin ALGORITHM (Time Quantum Scheduling)")
    print("")
    choice = int(input("ENTER A NUMBER: "))
    print("")
    if choice not in [1, 2, 3, 4]:
        print("Invalid choice! Please enter a number between 1 and 4.")
        return
    print("How do you want to provide process data?")
    print("1. Manual input")
    print("2. Load from processes.csv")
    mode = int(input("Enter 1 or 2: "))
    if mode == 2:
        filename = "processes.csv"
        need_priority = (choice == 3)  # Only Priority algorithm needs priority
        processes = load_processes_from_csv(filename, need_priority=need_priority)
    else:
        need_priority = (choice == 3)
        processes = get_manual_input(need_priority=need_priority)
    if choice == 1:
        fcfs = FCFS()
        fcfs.processData(processes)
        plt.show()
    elif choice == 2:
        sjf = SJF()
        sjf.processData(processes)
        plt.show()
    elif choice == 3:
        priority = Priority()
        priority.processData(processes)
        plt.show()
    elif choice == 4:
        rr = RoundRobin()
        rr.processData(processes)
        plt.show()

if __name__ == "__main__":
    main()