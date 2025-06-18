# Priority CPU Scheduling Algorithm
# This algorithm executes processes based on their priority level
# Higher priority processes are executed first
# This implementation is preemptive priority scheduling

from tabulate import tabulate

class Priority:
    """
    Priority CPU Scheduling Algorithm Implementation
    
    Priority scheduling is a scheduling algorithm that selects the process with the
    highest priority for execution. This implementation is preemptive, meaning a
    running process can be interrupted if a process with higher priority arrives.
    
    Process data structure: [PID, Arrival, Remaining_Burst, Priority, Completed, Original_Burst]
    
    Advantages:
    - Allows for process prioritization
    - Good for real-time systems
    - Can handle different process importance levels
    
    Disadvantages:
    - Can cause starvation for low priority processes
    - Requires priority assignment (can be subjective)
    - Indefinite blocking possible
    """

    def processData(self, no_of_processes):
        """
        Collect process information from user input
        
        Args:
            no_of_processes (int): Number of processes to schedule
            
        Process data structure: [PID, Arrival, Burst, Priority, Completed, Original_Burst]
        """
        process_data = []
        print(f"\nEnter details for {no_of_processes} processes:")
        print("Note: Higher priority number means higher priority (executes first)")
        
        for i in range(no_of_processes):
            temporary = []
            process_id = int(input("Enter Process ID: "))
            arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
            burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
            priority = int(input(f"Enter Priority for Process {process_id}: "))
            
            # Store process information: [PID, Arrival, Remaining_Burst, Priority, Completed, Original_Burst]
            # Remaining_Burst starts equal to Burst, Completed starts as 0 (False)
            temporary.extend([process_id, arrival_time, burst_time, priority, 0, burst_time])
            process_data.append(temporary)
        
        # Start the Priority scheduling algorithm
        Priority.schedulingProcess(self, process_data)

    def schedulingProcess(self, process_data):
        """
        Execute the preemptive Priority scheduling algorithm
        
        Priority Algorithm Steps:
        1. Sort processes by arrival time initially
        2. At each time unit, select the process with highest priority from ready queue
        3. Execute the selected process for 1 time unit
        4. Update remaining burst time and check if process is completed
        5. Repeat until all processes are completed
        
        Args:
            process_data (list): List of processes with [PID, Arrival, Remaining_Burst, Priority, Completed, Original_Burst]
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
                if process_data[i][1] <= s_time and process_data[i][4] == 0:
                    # Process has arrived and is not completed - add to ready queue
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][3], process_data[i][5]])
                    ready_queue.append(temp)
                    temp = []
                elif process_data[i][4] == 0:
                    # Process hasn't arrived yet - add to normal queue
                    # FIXED: Include priority in normal_queue data structure
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][3], process_data[i][5]])
                    normal_queue.append(temp)
                    temp = []
            
            # Exit condition: no processes in either queue
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            
            # Execute process from ready queue (if available)
            if len(ready_queue) != 0:
                # Sort ready queue by priority (highest priority first - reverse=True)
                ready_queue.sort(key=lambda x: x[3], reverse=True)
                
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
                    process_data[k][4] = 1  # Mark as completed
                    process_data[k].append(e_time)  # Add completion time
            
            # If no ready processes, execute from normal queue
            if len(ready_queue) == 0:
                # Sort normal queue by arrival time and jump to next arrival
                normal_queue.sort(key=lambda x: x[1])
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
                    process_data[k][4] = 1  # Mark as completed
                    process_data[k].append(e_time)  # Add completion time
        
        # Calculate performance metrics
        t_time = Priority.calculateTurnaroundTime(self, process_data)
        w_time = Priority.calculateWaitingTime(self, process_data)
        
        # Display the results
        Priority.printData(self, process_data, t_time, w_time, sequence_of_process)

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
            turnaround_time = process_data[i][6] - process_data[i][1]
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
            waiting_time = process_data[i][7] - process_data[i][5]
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
        headers = ["P ID", "AT", "Rem_BT", "Priority", "Completed", "BT", "CT", "TAT", "WT"]
        
        # Extract display data (all columns except the last two, then add TAT and WT)
        data = [row[:-2] + [row[-2], row[-1]] for row in process_data] 
        
        # Create and display the formatted table
        table = tabulate(data, headers=headers, tablefmt="fancy_grid")
        print("\nPriority Scheduling Results:")
        print(table)
        
        # Display Gantt chart sequence
        print(f'\nGantt Chart Sequence:')
        print(sequence_of_process)
        
        # Display performance metrics
        print("")
        print(f'1) Average Waiting Time: {average_waiting_time:.2f}')
        print(f'2) Average Turnaround Time: {average_turnaround_time:.2f}')
        print("\n" + "="*60)
