# Priority CPU Scheduling Algorithm
# This algorithm executes processes based on their priority level
# Higher priority processes are executed first
# This implementation is preemptive priority scheduling

from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Priority:
    """
    Priority CPU Scheduling Algorithm Implementation
    
    Priority scheduling is a preemptive scheduling algorithm where processes are
    executed based on their priority level. Higher priority processes are executed first.
    
    Process data structure: [PID, Arrival, Burst, Priority]
    
    Advantages:
    - Allows for priority-based execution
    - Good for real-time systems
    - Can handle different process importance levels
    
    Disadvantages:
    - Can cause starvation for low-priority processes
    - Priority inversion problem
    - Requires priority assignment mechanism
    """

    def processData(self, process_data):
        """
        Process the scheduling data for Priority algorithm
        
        Args:
            process_data (list): List of processes with [PID, Arrival, Burst, Priority] format
        """
        # Prepare data structure: [PID, Arrival, Remaining_Burst, Priority, Completed, Original_Burst]
        for i in range(len(process_data)):
            if len(process_data[i]) == 4:
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
                if process_data[i][1] <= s_time and process_data[i][4] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][3], process_data[i][5]])
                    ready_queue.append(temp)
                    temp = []
                elif process_data[i][4] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][3], process_data[i][5]])
                    normal_queue.append(temp)
                    temp = []
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[3], reverse=True)
                start_time.append(s_time)
                s_time = s_time + 1
                e_time = s_time
                exit_time.append(e_time)
                sequence_of_process.append(ready_queue[0][0])
                for k in range(len(process_data)):
                    if process_data[k][0] == ready_queue[0][0]:
                        break
                process_data[k][2] = process_data[k][2] - 1
                # Always append a Gantt segment for each time unit
                gantt.append((process_data[k][0], s_time - 1, s_time))
                if process_data[k][2] == 0:
                    process_data[k][4] = 1
                    process_data[k].append(e_time)
            if len(ready_queue) == 0:
                normal_queue.sort(key=lambda x: x[1])
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
                # Always append a Gantt segment for each time unit
                gantt.append((process_data[k][0], s_time - 1, s_time))
                if process_data[k][2] == 0:
                    process_data[k][4] = 1
                    process_data[k].append(e_time)
        t_time = Priority.calculateTurnaroundTime(self, process_data)
        w_time = Priority.calculateWaitingTime(self, process_data)
        Priority.printData(self, process_data, t_time, w_time, sequence_of_process)
        self.plot_gantt(gantt)

    def calculateTurnaroundTime(self, process_data):
        
        total_turnaround_time = 0
        for i in range(len(process_data)):
            # Turnaround Time = Completion Time - Arrival Time
            turnaround_time = process_data[i][6] - process_data[i][1]
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        
        average_turnaround_time = total_turnaround_time / len(process_data)
        return average_turnaround_time

    def calculateWaitingTime(self, process_data):
        
        total_waiting_time = 0
        for i in range(len(process_data)):
            # Waiting Time = Turnaround Time - Original Burst Time
            waiting_time = process_data[i][7] - process_data[i][5]
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        
        average_waiting_time = total_waiting_time / len(process_data)
        return average_waiting_time

    def printData(self, process_data, average_turnaround_time, average_waiting_time, sequence_of_process):
        
        # Sort processes by Process ID for consistent display
        process_data.sort(key=lambda x: x[0])
       
        headers = ["P ID", "AT", "Rem_BT", "Priority", "Completed", "BT", "CT", "TAT", "WT"]
        
        data = [row[:9] for row in process_data]
        
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print("\nPriority Scheduling Results:")
        print(table)
        
        
        print(f'\nGantt Chart Sequence:')
        print(sequence_of_process)
        
        
        print("")
        print(f'1) Average Waiting Time: {average_waiting_time:.2f}')
        print(f'2) Average Turnaround Time: {average_turnaround_time:.2f}')
        print("\n" + "="*60)

    def plot_gantt(self, gantt):
        fig, ax = plt.subplots()
        colors = list(mcolors.TABLEAU_COLORS.values())
        unique_pids = []
        for pid, _, _ in gantt:
            if pid not in unique_pids:
                unique_pids.append(pid)
        pid_to_color = {pid: colors[i % len(colors)] for i, pid in enumerate(unique_pids)}
        for (pid, start, end) in gantt:
            ax.barh(0, end-start, left=start, height=0.3, align='center', color=pid_to_color[pid])
            ax.text((start+end)/2, 0, f'P{pid}', va='center', ha='center', color='white', fontsize=10)
        ax.set_yticks([])
        ax.set_xlabel('Time')
        ax.set_title('Priority Scheduling Gantt Chart')
