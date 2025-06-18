# Round Robin CPU Scheduling Algorithm
# This algorithm gives each process a fixed time quantum (time slice)
# Processes are executed in a circular queue manner
# This implementation is preemptive Round Robin

from tabulate import tabulate

class RoundRobin:
    """
    Round Robin CPU Scheduling Algorithm Implementation
    
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

    def processData(self, no_of_processes):
        """
        Collect process information from user input
        
        Args:
            no_of_processes (int): Number of processes to schedule
            
        Process data structure: [PID, Arrival, Burst, Completed, Original_Burst]
        """
        process_data = []
        print(f"\nEnter details for {no_of_processes} processes:")
        print("Note: Time quantum determines how long each process runs before switching")
        
        for i in range(no_of_processes):
            temporary = []
            process_id = int(input("Enter Process ID: "))
            arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
            burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
            
            # Store process information: [PID, Arrival, Remaining_Burst, Completed, Original_Burst]
            # Remaining_Burst starts equal to Burst, Completed starts as 0 (False)
            temporary.extend([process_id, arrival_time, burst_time, 0, burst_time])
            process_data.append(temporary)

        # Get time quantum from user
        time_slice = int(input("Enter Time Quantum (Time Slice): "))
        print(f"Time Quantum: {time_slice} time units")
        
        # Start the Round Robin scheduling algorithm
        RoundRobin.schedulingProcess(self, process_data, time_slice)

    def schedulingProcess(self, process_data, time_slice):
        """
        Execute the Round Robin scheduling algorithm
        
        Round Robin Algorithm Steps:
        1. Sort processes by arrival time initially
        2. Add arrived processes to ready queue
        3. Execute first process in ready queue for time quantum or until completion
        4. If process doesn't complete, add it back to end of ready queue
        5. If process completes, remove it from queue
        6. Repeat until all processes are completed
        
        Args:
            process_data (list): List of processes with [PID, Arrival, Remaining_Burst, Completed, Original_Burst]
            time_slice (int): Time quantum for each process
        """
        start_time = []      # Track when each process starts execution
        exit_time = []       # Track when each process finishes execution
        executed_process = []  # Order of process execution for Gantt chart
        ready_queue = []     # Queue of processes ready to execute
        s_time = 0           # Current system time (CPU clock)
        
        # Sort processes by arrival time initially
        process_data.sort(key=lambda x: x[1])

        # Main scheduling loop - continues until all processes are completed
        while 1:
            normal_queue = []   # Processes that haven't arrived yet
            temp = []
            
            # Check all processes and add arrived ones to ready queue
            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    # Process has arrived and is not completed
                    present = 0
                    
                    # Check if process is already in ready queue
                    if len(ready_queue) != 0:
                        for k in range(len(ready_queue)):
                            if process_data[i][0] == ready_queue[k][0]:
                                present = 1
                    
                    # Add to ready queue if not already present
                    if present == 0:
                        temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                        ready_queue.append(temp)
                        temp = []
                    
                    # Move the last executed process to end of ready queue (if it exists)
                    if len(ready_queue) != 0 and len(executed_process) != 0:
                        for k in range(len(ready_queue)):
                            if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                                ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                
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
                if ready_queue[0][2] > time_slice:
                    # Process needs more time than quantum - execute for full quantum
                    start_time.append(s_time)
                    s_time = s_time + time_slice
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    
                    # Update the process in process_data
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    
                    # Decrease remaining burst time by time quantum
                    process_data[j][2] = process_data[j][2] - time_slice
                    ready_queue.pop(0)  # Remove from front of queue
                
                elif ready_queue[0][2] <= time_slice:
                    # Process can complete within quantum - execute until completion
                    start_time.append(s_time)
                    s_time = s_time + ready_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    
                    # Update the process in process_data
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    
                    # Process is completed
                    process_data[j][2] = 0
                    process_data[j][3] = 1  # Mark as completed
                    process_data[j].append(e_time)  # Add completion time
                    ready_queue.pop(0)  # Remove from queue
            
            # If no ready processes, execute from normal queue
            elif len(ready_queue) == 0:
                # Jump to arrival time of next process
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                
                if normal_queue[0][2] > time_slice:
                    # Process needs more time than quantum
                    start_time.append(s_time)
                    s_time = s_time + time_slice
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    
                    # Update the process in process_data
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    
                    # Decrease remaining burst time by time quantum
                    process_data[j][2] = process_data[j][2] - time_slice
                
                elif normal_queue[0][2] <= time_slice:
                    # Process can complete within quantum
                    start_time.append(s_time)
                    s_time = s_time + normal_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    
                    # Update the process in process_data
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    
                    # Process is completed
                    process_data[j][2] = 0
                    process_data[j][3] = 1  # Mark as completed
                    process_data[j].append(e_time)  # Add completion time

        # Calculate performance metrics
        t_time = RoundRobin.calculateTurnaroundTime(self, process_data)
        w_time = RoundRobin.calculateWaitingTime(self, process_data)
        
        # Display the results
        RoundRobin.printData(self, process_data, t_time, w_time, executed_process)

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

    def printData(self, process_data, average_turnaround_time, average_waiting_time, executed_process):
        """
        Display the scheduling results in a formatted table
        
        Args:
            process_data (list): Complete process data with all calculated times
            average_turnaround_time (float): Average turnaround time
            average_waiting_time (float): Average waiting time
            executed_process (list): Order of process execution
        """
        # Sort processes by Process ID for consistent display
        process_data.sort(key=lambda x: x[0])
        
        # Define table headers
        headers = ["P ID", "AT", "Rem_BT", "Completed", "BT", "CT", "TAT", "WT"]
        
        # Extract display data (all columns except the last two, then add TAT and WT)
        data = [row[:-2] + [row[-2], row[-1]] for row in process_data]
        
        # Create and display the formatted table
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print("\nRound Robin Scheduling Results:")
        print(table)
        
        # Display Gantt chart sequence
        print(f'\nGantt Chart Sequence:')
        print(executed_process)
        
        # Display performance metrics
        print("")
        print(f'1) Average Waiting Time: {average_waiting_time:.2f}')
        print(f'2) Average Turnaround Time: {average_turnaround_time:.2f}')
        print("\n" + "="*60)