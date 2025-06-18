# SJF (Shortest Job First) CPU Scheduling Algorithm
# This algorithm executes the process with the shortest burst time first
# It can be preemptive (SJF-P) or non-preemptive (SJF-NP)
# This implementation is preemptive SJF

from tabulate import tabulate

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

    def processData(self, no_of_processes):
        """
        Collect process information from user input
        
        Args:
            no_of_processes (int): Number of processes to schedule
            
        Process data structure: [PID, Arrival, Burst, Completed, Original_Burst]
        """
        process_data = []
        print(f"\nEnter details for {no_of_processes} processes:")
        print("Note: Lower burst time means process executes faster")
        
        for i in range(no_of_processes):
            temporary = []
            process_id = int(input("Enter Process ID: "))
            arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
            burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
            
            # Store process information: [PID, Arrival, Remaining_Burst, Completed, Original_Burst]
            # Remaining_Burst starts equal to Burst, Completed starts as 0 (False)
            temporary.extend([process_id, arrival_time, burst_time, 0, burst_time])
            process_data.append(temporary)
        
        # Start the SJF scheduling algorithm
        SJF.schedulingProcess(self, process_data)

    def schedulingProcess(self, process_data):
        """
        Execute the preemptive SJF scheduling algorithm
        
        SJF Algorithm Steps:
        1. Sort processes by arrival time initially
        2. At each time unit, select the process with shortest remaining burst time
        3. Execute the selected process for 1 time unit
        4. Update remaining burst time and check if process is completed
        5. Repeat until all processes are completed
        
        Args:
            process_data (list): List of processes with [PID, Arrival, Remaining_Burst, Completed, Original_Burst]
        """
        start_time = []      # Track when each process starts execution
        exit_time = []       # Track when each process finishes execution
        s_time = 0           # Current system time (CPU clock)
        sequence_of_process = []  # Order of process execution for Gantt chart
        
        # Sort processes by arrival time initially
        process_data.sort(key=lambda x: x[1])

        # Main scheduling loop - continues until all processes are completed
        while 1:
            ready_queue = []    # Processes that have arrived and are ready to execute
            normal_queue = []   # Processes that haven't arrived yet
            temp = []
            
            # Separate processes into ready and normal queues
            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    # Process has arrived and is not completed - add to ready queue
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    ready_queue.append(temp)
                    temp = []
                elif process_data[i][3] == 0:
                    # Process hasn't arrived yet - add to normal queue
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    normal_queue.append(temp)
                    temp = []
            
            # Exit condition: no processes in either queue
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            
            # Execute process from ready queue (if available)
            if len(ready_queue) != 0:
                # Sort ready queue by remaining burst time (shortest first)
                ready_queue.sort(key=lambda x: x[2])
                
                start_time.append(s_time)
                s_time = s_time + 1  # Execute for 1 time unit
                e_time = s_time
                exit_time.append(e_time)
                sequence_of_process.append(ready_queue[0][0])
                
                # Find and update the selected process in process_data
                for k in range(len(process_data)):
                    if process_data[k][0] == ready_queue[0][0]:
                        break
                
                # Decrease remaining burst time by 1
                process_data[k][2] = process_data[k][2] - 1
                
                # Check if process is completed
                if process_data[k][2] == 0:
                    process_data[k][3] = 1  # Mark as completed
                    process_data[k].append(e_time)  # Add completion time
            
            # If no ready processes, execute from normal queue
            if len(ready_queue) == 0:
                # Jump to arrival time of next process
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                
                start_time.append(s_time)
                s_time = s_time + 1  # Execute for 1 time unit
                e_time = s_time
                exit_time.append(e_time)
                sequence_of_process.append(normal_queue[0][0])
                
                # Find and update the selected process in process_data
                for k in range(len(process_data)):
                    if process_data[k][0] == normal_queue[0][0]:
                        break
                
                # Decrease remaining burst time by 1
                process_data[k][2] = process_data[k][2] - 1
                
                # Check if process is completed
                if process_data[k][2] == 0:
                    process_data[k][3] = 1  # Mark as completed
                    process_data[k].append(e_time)  # Add completion time
        
        # Calculate performance metrics
        t_time = SJF.calculateTurnaroundTime(self, process_data)
        w_time = SJF.calculateWaitingTime(self, process_data)
        
        # Display the results
        SJF.printData(self, process_data, t_time, w_time, sequence_of_process)

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
            # Turnaround Time = Completion Time - Arrival Time
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
            # Waiting Time = Turnaround Time - Original Burst Time
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
        # Sort processes by Process ID for consistent display
        process_data.sort(key=lambda x: x[0])
        
        # Define table headers
        headers = ["P ID", "AT", "Rem_BT", "Completed", "BT", "CT", "TT", "WT"]
        
        # Extract display data (all columns except the last two, then add TT and WT)
        data = [row[:-2] + [row[-2], row[-1]] for row in process_data]
        
        # Create and display the formatted table
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print("\nSJF Scheduling Results:")
        print(table)
        
        # Display Gantt chart sequence
        print(f'\nGantt Chart Sequence:')
        print(sequence_of_process)
        
        # Display performance metrics
        print("")
        print(f'1) Average Waiting Time: {average_waiting_time:.2f}')
        print(f'2) Average Turnaround Time: {average_turnaround_time:.2f}')
        print("\n" + "="*60)