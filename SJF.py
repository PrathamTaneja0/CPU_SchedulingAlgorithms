# SJF (Shortest Job First) CPU Scheduling Algorithm
# This algorithm executes the process with the shortest burst time first
# It can be preemptive (SJF-P) or non-preemptive (SJF-NP)
# This implementation is preemptive SJF

from tabulate import tabulate
import matplotlib.pyplot as plt

class SJF:
    """
    Shortest Job First (SJF) CPU Scheduling Algorithm Implementation
    
    SJF is a scheduling algorithm that selects the process with the smallest burst time
    for execution. This implementation is preemptive, meaning a running process can be
    interrupted if a process with shorter burst time arrives.
    
    Process data structure: [PID, Arrival, Remaining_Burst, Completed, Original_Burst]
    
    Advantages:
    - Minimizes average waiting time
    - Optimal for minimizing average turnaround time
    
    Disadvantages:
    - Can cause starvation for long processes
    - Requires knowledge of burst times (not always available)
    - Complex implementation
    """

    def processData(self, process_data):
        """
        Process the scheduling data for SJF algorithm
        
        Args:
            process_data (list): List of processes with [PID, Arrival, Burst] format
        """
        # Prepare data structure: [PID, Arrival, Remaining_Burst, Completed, Original_Burst]
        for i in range(len(process_data)):
            if len(process_data[i]) == 3:
                # Add Completed=0 and Original_Burst
                process_data[i].extend([0, process_data[i][2]])
        
        start_time = []
        exit_time = []
        s_time = 0
        sequence_of_process = []
        gantt = []
        process_data.sort(key=lambda x: x[1])
        while 1:
            ready_queue = []
            normal_queue = []
            temp = []
            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    ready_queue.append(temp)
                    temp = []
                elif process_data[i][3] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    normal_queue.append(temp)
                    temp = []
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                start_time.append(s_time)
                s_time = s_time + 1
                e_time = s_time
                exit_time.append(e_time)
                sequence_of_process.append(ready_queue[0][0])
                for k in range(len(process_data)):
                    if process_data[k][0] == ready_queue[0][0]:
                        break
                process_data[k][2] = process_data[k][2] - 1
                if process_data[k][2] == 0:
                    process_data[k][3] = 1
                    process_data[k].append(e_time)
                    gantt.append((process_data[k][0], e_time - process_data[k][4], e_time))
            if len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                start_time.append(s_time)
                s_time = s_time + 1
                e_time = s_time
                exit_time.append(e_time)
                sequence_of_process.append(normal_queue[0][0])
                for k in range(len(process_data)):
                    if process_data[k][0] == normal_queue[0][0]:
                        break
                process_data[k][2] = process_data[k][2] - 1
                if process_data[k][2] == 0:
                    process_data[k][3] = 1
                    process_data[k].append(e_time)
                    gantt.append((process_data[k][0], e_time - process_data[k][4], e_time))
        t_time = SJF.calculateTurnaroundTime(self, process_data)
        w_time = SJF.calculateWaitingTime(self, process_data)
        SJF.printData(self, process_data, t_time, w_time, sequence_of_process)
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
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][5] - process_data[i][1]
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        average_turnaround_time = total_turnaround_time / len(process_data)
        return average_turnaround_time

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
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i][6] - process_data[i][4]
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        average_waiting_time = total_waiting_time / len(process_data)
        return average_waiting_time

    def printData(self, process_data, average_turnaround_time, average_waiting_time, sequence_of_process):
        """
        Display the scheduling results in a formatted table
        
        Args:
            process_data (list): Complete process data with all calculated times
            average_turnaround_time (float): Average turnaround time
            average_waiting_time (float): Average waiting time
            sequence_of_process (list): Order of process execution
        """
        process_data.sort(key=lambda x: x[0])
        headers = ["P ID", "AT", "Rem_BT", "Completed", "BT", "CT", "TT", "WT"]
        data = [row[:8] for row in process_data]
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print("\nSJF Scheduling Results:")
        print(table)
        print(f'\nGantt Chart Sequence:')
        print(sequence_of_process)
        print("")
        print(f'1) Average Waiting Time: {average_waiting_time:.2f}')
        print(f'2) Average Turnaround Time: {average_turnaround_time:.2f}')
        print("\n" + "="*60)

    def plot_gantt(self, gantt):
        fig, ax = plt.subplots()
        for i, (pid, start, end) in enumerate(gantt):
            ax.barh(0, end-start, left=start, height=0.3, align='center', label=f'P{pid}' if i==0 else "")
            ax.text((start+end)/2, 0, f'P{pid}', va='center', ha='center', color='white', fontsize=10)
        ax.set_yticks([])
        ax.set_xlabel('Time')
        ax.set_title('SJF Gantt Chart')