# Round Robin CPU Scheduling Algorithm
# This algorithm gives each process a fixed time quantum (time slice)
# Processes are executed in a circular queue manner
# This implementation is preemptive Round Robin

from tabulate import tabulate
import matplotlib.pyplot as plt
from collections import deque

class RoundRobin:
    """
    Round Robin CPU Scheduling Algorithm Implementation
    Uses collections.deque for the ready queue and supports Gantt chart visualization.
    
    Round Robin is a preemptive scheduling algorithm that assigns a fixed time quantum
    to each process. If a process doesn't complete within its time quantum, it's moved
    to the end of the ready queue and the next process gets the CPU.
    
    Process data structure: [PID, Arrival, Remaining_Burst, Completed, Original_Burst]
    
    Advantages:
    - Fair scheduling - each process gets equal CPU time
    - No starvation - every process gets CPU time
    - Good for time-sharing systems
    - Predictable response time
    
    Disadvantages:
    - Performance depends heavily on time quantum size
    - Context switching overhead
    - May not be optimal for all scenarios
    """

    def processData(self, process_data):
        """
        Accepts a list of process data: [PID, Arrival, Burst] or [PID, Arrival, Burst, ...]
        Prompts for time quantum, then runs the scheduling algorithm.
        """
        # Ensure process_data has [PID, Arrival, Remaining_Burst, Completed, Original_Burst]
        for i in range(len(process_data)):
            if len(process_data[i]) == 3:
                # Add Completed=0 and Original_Burst
                process_data[i].extend([0, process_data[i][2]])
            elif len(process_data[i]) == 4:
                # Add Completed=0 and Original_Burst if not present
                if len(process_data[i]) == 4:
                    process_data[i].extend([0, process_data[i][2]])
        time_slice = int(input("Enter Time Quantum (Time Slice): "))
        print(f"Time Quantum: {time_slice} time units")
        self.schedulingProcess(process_data, time_slice)

    def schedulingProcess(self, process_data, time_slice):
        """
        Executes the Round Robin scheduling algorithm using a deque for the ready queue.
        Generates a Gantt chart of process execution.
        """
        s_time = 0
        ready_queue = deque()
        gantt = []
        process_data.sort(key=lambda x: x[1])
        n = len(process_data)
        completed = 0
        mark = [0] * n
        while completed < n:
            for i in range(n):
                if process_data[i][1] <= s_time and process_data[i][3] == 0 and mark[i] == 0:
                    ready_queue.append(i)
                    mark[i] = 1
            if not ready_queue:
                s_time += 1
                continue
            idx = ready_queue.popleft()
            pid, arrival, rem_bt, completed_flag, orig_bt = process_data[idx]
            exec_time = min(rem_bt, time_slice)
            start_time = s_time
            s_time += exec_time
            process_data[idx][2] -= exec_time
            gantt.append((pid, start_time, s_time))
            for i in range(n):
                if process_data[i][1] <= s_time and process_data[i][3] == 0 and mark[i] == 0:
                    ready_queue.append(i)
                    mark[i] = 1
            if process_data[idx][2] == 0 and process_data[idx][3] == 0:
                process_data[idx][3] = 1
                process_data[idx].append(s_time)  # Completion time
                completed += 1
            elif process_data[idx][2] > 0:
                ready_queue.append(idx)
        avg_tat = self.calculateTurnaroundTime(process_data)
        avg_wt = self.calculateWaitingTime(process_data)
        self.printData(process_data, avg_tat, avg_wt)
        self.plot_gantt(gantt)

    def calculateTurnaroundTime(self, process_data):
        """
        Calculate turnaround time for each process and average
        
        Turnaround Time = Completion Time - Arrival Time
        This measures the total time from arrival to completion
        
        Args:
            process_data (list): List of processes with completion times added
            
        Returns:
            float: Average turnaround time
        """
        total_tat = 0
        for proc in process_data:
            tat = proc[5] - proc[1]
            proc.append(tat)
            total_tat += tat
        return total_tat / len(process_data)

    def calculateWaitingTime(self, process_data):
        """
        Calculate waiting time for each process and average
        
        Waiting Time = Turnaround Time - Original Burst Time
        This measures the time a process spends waiting in the ready queue
        
        Args:
            process_data (list): List of processes with turnaround times added
            
        Returns:
            float: Average waiting time
        """
        total_wt = 0
        for proc in process_data:
            wt = proc[6] - proc[4]
            proc.append(wt)
            total_wt += wt
        return total_wt / len(process_data)

    def printData(self, process_data, avg_tat, avg_wt):
        """
        Display the scheduling results in a formatted table
        
        Args:
            process_data (list): Complete process data with all calculated times
            avg_tat (float): Average turnaround time
            avg_wt (float): Average waiting time
        """
        headers = ["P ID", "AT", "Rem_BT", "Completed", "BT", "CT", "TAT", "WT"]
        data = [row[:8] for row in process_data]
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print("\nRound Robin Scheduling Results:")
        print(table)
        print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
        print(f"Average Waiting Time:    {avg_wt:.2f}")
        print("\n" + "="*60)

    def plot_gantt(self, gantt):
        fig, ax = plt.subplots()
        for i, (pid, start, end) in enumerate(gantt):
            ax.barh(0, end-start, left=start, height=0.3, align='center', label=f'P{pid}' if i==0 else "")
            ax.text((start+end)/2, 0, f'P{pid}', va='center', ha='center', color='white', fontsize=10)
        ax.set_yticks([])
        ax.set_xlabel('Time')
        ax.set_title('Round Robin Gantt Chart')
        plt.show()