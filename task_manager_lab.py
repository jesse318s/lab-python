import tkinter as tk
import multiprocessing
import threading
import time
import re
import psutil

# Task class to represent a task
class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False

    def mark_completed(self):
        self.completed = True

# Function to update the task list display
def update_task_list():
    task_list.delete(0, tk.END)

    for i, task in enumerate(tasks):
        status = "Completed" if task.completed else "Pending"
        task_list.insert(tk.END, f"{i + 1}. {task.description} - {status}")

# Function to add a task
def add_task(description):
    if re.match(r'^[a-zA-Z0-9\s]+$', description): # Ensure the description is alphanumeric
        task = Task(description)
        tasks.append(task)
        update_task_list()
    else:
        print("Invalid task description. Only alphanumeric characters and spaces are allowed.")

# Function to handle adding multiple tasks from the GUI
def handle_add():
    descriptions = task_entry.get().split(',')

    for description in descriptions:
        add_task(description.strip())

    task_entry.delete(0, tk.END)

# Callback function to update the task list after a task is completed
def task_completed_callback(index):
    tasks[index].mark_completed()
    print(f"Task {index + 1} completed")
    update_task_list()

# Function to mark a task as completed
def complete_task(index):
    # Simulate a long-running task
    time.sleep(3)

    return index

# Function to handle completing task(s) from the GUI
def handle_complete():
    indices = complete_entry.get().split(',')

    for index in indices:
        if not index.strip().isdigit():
            print(f"Invalid index: {index.strip()}")

            continue
        
        idx = int(index.strip()) - 1

        if idx not in range(len(tasks)):
            print(f"Index {idx + 1} is out of range")

            continue

        try:
            print(f"Submitting task {int(index.strip())} for completion")
            pool.apply_async(complete_task, args=(idx,), callback=task_completed_callback)
        except Exception as e:
            print(f"An error occurred while submitting task {int(index.strip())} for completion: {e}")

    complete_entry.delete(0, tk.END)

# Function to print state when battery is low
def print_state():
    for task in tasks:
        print(f"{task.description} - {'Completed' if task.completed else 'Pending'}")

# Function to monitor battery status
def monitor_battery():
    while True:
        battery = psutil.sensors_battery()

        if battery.percent < 10:
            print_state()

            break

        time.sleep(60)

# Main function
if __name__ == '__main__':
    tasks = []

    # Create the main application window
    root = tk.Tk()
    root.title("Task Manager")

    # Task entry field
    task_entry = tk.Entry(root, width=50)
    task_entry.pack(pady=10)

    # Add task(s) button
    add_button = tk.Button(root, text="Add Task(s) (comma-separated)", command=handle_add)
    add_button.pack(pady=5)

    # Task list display
    task_list = tk.Listbox(root, width=50)
    task_list.pack(pady=10)

    # Complete task(s) entry field
    complete_entry = tk.Entry(root, width=50)
    complete_entry.pack(pady=10)

    # Complete task(s) button
    complete_button = tk.Button(root, text="Complete Task(s) (comma-separated)", command=handle_complete)
    complete_button.pack(pady=5)

    # Create a pool of worker processes
    pool = multiprocessing.Pool(processes=4)

    # Start the battery monitoring thread
    battery_thread = threading.Thread(target=monitor_battery)
    battery_thread.daemon = True
    battery_thread.start()

    # Start the GUI event loop
    root.mainloop()

    # Close the pool and wait for the worker processes to finish
    pool.close()
    pool.join()

    print('All workers completed')