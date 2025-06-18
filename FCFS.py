# FCFS (First Come First Serve) CPU Scheduling Algorithm
# This algorithm executes processes in the order they arrive (FIFO - First In, First Out)
# It's the simplest scheduling algorithm but may not be the most efficient

from tabulate import tabulate

class FCFS:
    """
    First Come First Serve (FCFS) CPU Scheduling Algorithm Implementation
    
    FCFS is a non-preemptive scheduling algorithm where processes are executed
    in the order they arrive. The process that arrives first gets the CPU first.
    
    Advantages:
    - Simple to understand and implement
    - No starvation (every process gets CPU time)
    
    Disadvantages:
    - Poor performance for processes with varying burst times
    - High average waiting time
    - Not suitable for time-sharing systems
    """
    
    def processData(self, no_of_processes):
        """
        Collect process information from user input
        
        Args:
            no_of_processes (int): Number of processes to schedule
            
        Process data structure: [process_id, arrival_time, burst_time]
        """
        process_data = []
        print(f"\nEnter details for {no_of_processes} processes:")
        print("Note: Lower arrival time means process arrives earlier")
        
        for i in range(no_of_processes):
            temporary = []
            process_id = int(input("Enter Process ID: "))
            arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
            burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
            
            # Store process information: [PID, Arrival, Burst]
            temporary.extend([process_id, arrival_time, burst_time])
            process_data.append(temporary)
        
        # Start the FCFS scheduling algorithm
        self.schedulingProcess(process_data)

    def schedulingProcess(self, process_data):
        """
        Execute the FCFS scheduling algorithm
        
        FCFS Algorithm Steps:
        1. Sort processes by arrival time (and burst time as tiebreaker)
        2. Execute each process completely before moving to the next
        3. Calculate completion time, turnaround time, and waiting time
        
        Args:
            process_data (list): List of processes with [PID, Arrival, Burst]
        """
        # Sort processes by arrival time first, then by burst time (for processes with same arrival)
        process_data.sort(key=lambda x: (x[1], x[2]))
        
        s_time = 0  # Current system time (CPU clock)
        
        for idx, proc in enumerate(process_data):
            # If CPU is idle (no process has arrived yet), jump to the next arrival time
            if s_time < proc[1]:
                s_time = proc[1]
            
            # Start time is the current system time
            start_time = s_time
            
            # Advance the clock by the burst time of current process
            s_time += proc[2]
            
            # Completion time is the new system time
            completion_time = s_time
            
            # Append completion time to the process record
            proc.append(completion_time)

        # Calculate performance metrics
        avg_tat = self.calculateTurnaroundTime(process_data)
        avg_wt  = self.calculateWaitingTime(process_data)
        
        # Create sequence of execution for Gantt chart
        sequence = [row[0] for row in process_data]

        # Display the results
        self.printData(process_data, avg_tat, avg_wt, sequence)

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
            # Turnaround Time = Completion Time - Arrival Time
            tat = proc[3] - proc[1]   # completion - arrival
            proc.append(tat)
            total_tat += tat
        
        return total_tat / len(process_data)

    def calculateWaitingTime(self, process_data):
        """
        Calculate waiting time for each process and average
        
        Waiting Time = Turnaround Time - Burst Time
        This measures the time a process spends waiting in the ready queue
        
        Args:
            process_data (list): List of processes with turnaround times added
            
        Returns:
            float: Average waiting time
        """
        total_wt = 0
        for proc in process_data:
            # Waiting Time = Turnaround Time - Burst Time
            wt = proc[4] - proc[2]    # turnaround - burst
            proc.append(wt)
            total_wt += wt
        
        return total_wt / len(process_data)

    def printData(self, process_data, avg_tat, avg_wt, sequence):
        """
        Display the scheduling results in a formatted table
        
        Args:
            process_data (list): Complete process data with all calculated times
            avg_tat (float): Average turnaround time
            avg_wt (float): Average waiting time
            sequence (list): Order of process execution
        """
        # Define table headers
        headers = ["Process ID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"]
        
        # Extract only the display columns from each process record
        data = [row[0:6] for row in process_data]
        
        # Create and display the formatted table
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print("\nFCFS Scheduling Results:")
        print(table)
        
        # Display Gantt chart sequence
        print("\nGantt Chart Sequence:", sequence)
        
        # Display performance metrics
        print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
        print(f"Average Waiting Time:    {avg_wt:.2f}")
        print("\n" + "="*60)
