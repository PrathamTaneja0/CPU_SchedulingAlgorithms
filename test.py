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
        # Read all lines and filter out comments
        lines = csvfile.readlines()
        # Find the header line (first non-comment line)
        header_line = None
        for line in lines:
            if not line.strip().startswith('#'):
                header_line = line
                break
        
        if header_line is None:
            raise ValueError("No valid header found in CSV file")
        
        # Create a new file-like object with only non-comment lines
        filtered_lines = [header_line]  # Start with header
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                filtered_lines.append(line + '\n')
        
        # Create a StringIO object to simulate a file
        from io import StringIO
        csv_content = StringIO(''.join(filtered_lines))
        
        reader = csv.DictReader(csv_content)
        for row in reader:
            try:
                pid = int(row['PID'])
                arrival = int(row['Arrival'])
                burst = int(row['Burst'])
                priority = int(row['Priority']) if 'Priority' in row and row['Priority'] != '' else None
                if priority is not None:
                    processes.append([pid, arrival, burst, priority])
                else:
                    processes.append([pid, arrival, burst])
            except ValueError as e:
                print(f"Warning: Skipping invalid row: {row}")
                continue
    return processes

def get_test_cases():
    """Extract test cases from CSV file with their descriptions"""
    test_cases = []
    current_test = None
    current_processes = []
    test_case_number = 0
    
    with open('test.csv', 'r') as file:
        lines = file.readlines()
        
    for line in lines:
        line = line.strip()
        if line.startswith('# Test Case'):
            # Save previous test case if exists
            if current_test and current_processes:
                test_cases.append({
                    'name': current_test,
                    'processes': current_processes.copy()
                })
            
            # Start new test case
            current_test = line
            current_processes = []
        elif line.startswith('# Priority') and not line.startswith('# Test Case'):
            # Save previous test case if exists
            if current_test and current_processes:
                test_cases.append({
                    'name': current_test,
                    'processes': current_processes.copy()
                })
            
            # Start new Priority test case (Test Case 3)
            test_case_number += 1
            current_test = f"# Test Case 3: Priority Scheduling with Different Arrival Times"
            current_processes = []
        elif line and not line.startswith('#') and ',' in line:
            # This is a process line
            parts = line.split(',')
            if len(parts) >= 3:
                try:
                    pid = int(parts[0])
                    arrival = int(parts[1])
                    burst = int(parts[2])
                    priority = int(parts[3]) if len(parts) > 3 else 1
                    current_processes.append([pid, arrival, burst, priority])
                except ValueError:
                    continue
    
    # Add the last test case
    if current_test and current_processes:
        test_cases.append({
            'name': current_test,
            'processes': current_processes.copy()
        })
    
    return test_cases

def run_fcfs(processes):
    print("\n=== FCFS Test ===")
    fcfs = FCFS()
    #  [PID, Arrival, Burst] - create a copy
    proc = [p[:3].copy() for p in processes]
    fcfs.processData(proc)
    plt.show()

def run_sjf(processes):
    print("\n=== SJF Test ===")
    sjf = SJF()
    #  [PID, Arrival, Burst] - create a copy
    proc = [p[:3].copy() for p in processes]
    sjf.processData(proc)
    plt.show()

def run_priority(processes):
    print("\n=== Priority Test ===")
    priority = Priority()
    # [PID, Arrival, Burst, Priority] - create a copy
    proc = [p.copy() for p in processes]
    priority.processData(proc)
    plt.show()

def run_rr(processes, time_quantum=2):
    print(f"\n=== Round Robin Test (Time Quantum = {time_quantum}) ===")
    rr = RoundRobin()
    # [PID, Arrival, Burst] or [PID, Arrival, Burst, Priority] - create a copy
    proc = [p.copy() for p in processes]
    # Simulate input for time quantum
    old_stdin = sys.stdin
    sys.stdin = StringIO(f"{time_quantum}\n")
    try:
        rr.processData(proc)
        plt.show()
    finally:
        sys.stdin = old_stdin

def display_menu():
    print("\n" + "="*60)
    print("CPU SCHEDULING ALGORITHMS - TEST CASE RUNNER")
    print("="*60)
    
    test_cases = get_test_cases()
    
    print("\nAvailable Test Cases:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['name']}")
    
    print(f"\n{len(test_cases) + 1}. Exit")
    
    while True:
        try:
            choice = int(input(f"\nSelect test case (1-{len(test_cases) + 1}): "))
            if 1 <= choice <= len(test_cases):
                selected_test = test_cases[choice - 1]
                print(f"\nSelected: {selected_test['name']}")
                print(f"Processes: {selected_test['processes']}")
                
                # Algorithm selection
                print("\nSelect Algorithm:")
                print("1. FCFS (First Come First Serve)")
                print("2. SJF (Shortest Job First)")
                print("3. Priority Scheduling")
                print("4. Round Robin")
                print("5. Back to test case selection")
                
                algo_choice = int(input("Select algorithm (1-5): "))
                
                if algo_choice == 1:
                    run_fcfs(selected_test['processes'])
                elif algo_choice == 2:
                    run_sjf(selected_test['processes'])
                elif algo_choice == 3:
                    run_priority(selected_test['processes'])
                elif algo_choice == 4:
                    time_quantum = int(input("Enter time quantum: "))
                    run_rr(selected_test['processes'], time_quantum)
                elif algo_choice == 5:
                    display_menu()
                    return
                else:
                    print("Invalid choice!")
                    
                input("\nPress Enter to continue...")
                display_menu()
                return
                
            elif choice == len(test_cases) + 1:
                print("Goodbye!")
                return
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a valid number!")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return

def main():
    display_menu()

if __name__ == "__main__":
    main() 