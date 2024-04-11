import threading
import time

# Global variable
global_var = 0

# Function to update the global variable
def update_variable():
    global global_var
    while True:
        # Update the global variable
        global_var += 1
        time.sleep(1)  # Sleep for 1 second

# Function to listen and print the global variable
def print_variable():
    global global_var
    while True:
        # Print the global variable
        print("Global variable:", global_var)
        time.sleep(2)  # Sleep for 2 seconds

# Create threads for both functions
update_thread = threading.Thread(target=update_variable)
print_thread = threading.Thread(target=print_variable)

# Start both threads
update_thread.start()
print_thread.start()

# Join threads to the main thread
update_thread.join()
print_thread.join()
