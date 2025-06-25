from tabulate import tabulate
import matplotlib.pyplot as plt

class FCFS:
    """
    First-Come, First-Served (FCFS) CPU Scheduling Algorithm Implementation
    
    FCFS is a non-preemptive scheduling algorithm where processes are executed
    in the order they arrive. The process that arrives first gets the CPU first.
    
    Process data structure: [PID, Arrival, Burst]
    
    Advantages:
    - Simple to implement and understand
    - No starvation
    
    Disadvantages:
    - Poor performance for short processes behind long ones
    - High average waiting time
    - Not optimal for minimizing waiting time
    """
    
    def processData(self, process_data):
        # Sort by arrival time only (FCFS principle)
        process_data.sort(key=lambda x: x[1])
        s_time = 0
        gantt = []
        for idx, proc in enumerate(process_data):
            if s_time < proc[1]:
                s_time = proc[1]
            start_time = s_time
            s_time += proc[2]
            completion_time = s_time
            proc.append(completion_time)
            gantt.append((proc[0], start_time, completion_time))
        avg_tat = self.calculateTurnaroundTime(process_data)
        avg_wt  = self.calculateWaitingTime(process_data)
        self.printData(process_data, avg_tat, avg_wt)
        self.plot_gantt(gantt)

    def calculateTurnaroundTime(self, process_data):
        total_tat = 0
        for proc in process_data:
            tat = proc[3] - proc[1] # Completion time - Arrival time
            proc.append(tat)
            total_tat += tat
        return total_tat / len(process_data)

    def calculateWaitingTime(self, process_data):
        total_wt = 0
        for proc in process_data:
            wt = proc[4] - proc[2] # turnaround time - burst time
            proc.append(wt)
            total_wt += wt
        return total_wt / len(process_data)

    def printData(self, process_data, avg_tat, avg_wt):
        headers = ["Process ID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"]
        data = [row[:6] for row in process_data]
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print("\nFCFS Scheduling Results:")
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
        ax.set_title('FCFS Gantt Chart')
