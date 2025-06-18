from FCFS import FCFS
from SJF import SJF
from PriorityScheduling import Priority
from RoundRobin import RoundRobin

# Main execution block - this code runs when the script is executed directly
if __name__ == "__main__":
    # Display the main title and menu
    print("                                    ===== CPU SCHEDULING SIMULATOR =====")
    print("")
    
    # Start the main program loop
    

def Run():
    """
    Main function that displays the menu and handles user choices for different scheduling algorithms.
    This function runs in a loop until the user chooses to exit.
    """
    print('-'*125)
    print("WHICH ALGORITHM DO YOU WANT TO RUN?")
    print("")
    print("1. PRESS 1 FOR FCFS ALGORITHM (First Come First Serve)")
    print("2. PRESS 2 FOR SJF ALGORITHM (Shortest Job First)")
    print("3. PRESS 3 FOR Priority ALGORITHM (Priority-based Scheduling)")
    print("4. PRESS 4 FOR Round-Robin ALGORITHM (Time Quantum Scheduling)")
    print("")

    # Get user choice for algorithm selection
    choice = int(input("ENTER A NUMBER: "))
    print("")

    # Validate and process user choice
    if choice in [1, 2, 3, 4]:
        # Get number of processes from user
        no_of_processes = int(input("How many Processes do you want to run in the system? "))
        
        # Execute the selected algorithm
        if choice == 1:
            # First Come First Serve - processes are executed in order of arrival
            print("\n=== Running FCFS (First Come First Serve) Algorithm ===")
            fcfs = FCFS()
            fcfs.processData(no_of_processes)

        elif choice == 2:
            # Shortest Job First - processes with shortest burst time get priority
            print("\n=== Running SJF (Shortest Job First) Algorithm ===")
            sjf = SJF()
            sjf.processData(no_of_processes)

        elif choice == 3:
            # Priority Scheduling - processes with higher priority execute first
            print("\n=== Running Priority Scheduling Algorithm ===")
            priority = Priority()
            priority.processData(no_of_processes)

        elif choice == 4:
            # Round Robin - each process gets a fixed time quantum
            print("\n=== Running Round Robin Algorithm ===")
            rr = RoundRobin()
            rr.processData(no_of_processes)
        
        print("")
        # Ask if user wants to run another algorithm
        new = input("Do you want to run another Algorithm? (Y/N): ")
        print("")
        
        # Handle user response for continuing or exiting
        if new.upper() == 'Y':
            # Recursive call to run another algorithm
            Run()
        elif new.upper() == 'N':
            print("Thank you for using CPU Scheduling Simulator!")
        else:
            # Handle invalid input
            print("Please enter Y or N")
            new = input("Do you want to run another Algorithm? (Y/N): ")
            if new.upper() == 'Y':
                Run()
            else:
                print("Thank you for using CPU Scheduling Simulator!")
    else:
        # Handle invalid algorithm choice
        print("Invalid choice! Please enter a number between 1 and 4.")
        Run()

Run()