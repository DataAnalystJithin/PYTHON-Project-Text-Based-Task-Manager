# TEXT BASED TASK MANAGER
# BY - JITHIN JAYACHANDRAN

# A text-based task manager is a program or application that allows users to manage their tasks or to-do lists through a command-line interface (CLI) 
# or text-based user interface (TUI). Instead of using graphical elements like buttons and menus, users interact with the task manager by typing commands
# or selecting options from a list displayed in the terminal/console.

import os
import threading
import time
import datetime

# Decorator Function log_function_call
# This function is a decorator used to log function calls. It prints the function name, arguments, and keyword arguments when the decorated function is called.
# log_function_call: The outer function, which takes a boolean argument suppress_message to determine whether to suppress the log message.
# decorator: Inner function acting as the actual decorator.
# wrapper: Innermost function wrapping the original function, which prints the log message before calling the original function.

def log_function_call(suppress_message=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not suppress_message:
                print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Task Class
# Defines a Task class with attributes task_id, description, priority, and due_date. This class is a simple data structure representing a task.

class Task:
    def __init__(self, task_id, description, priority, due_date):
        self.task_id = task_id
        self.description = description
        self.priority = priority
        self.due_date = due_date


# TaskManager Class
# Defines a TaskManager class responsible for managing tasks. It includes methods for adding, deleting, displaying, and sorting tasks,
# as well as saving and loading tasks from a file.

class TaskManager:
    def __init__(self): 
        self.tasks = []
        self.task_id_counter = 1  # Initialize the task ID counter
        self.sorted_tasks = []  # Temporary sorted list of tasks


    @log_function_call(suppress_message=True)  # Suppress the message for add_task
    def add_task(self, description, priority, due_date): 
        task = Task(self.task_id_counter, description, priority, due_date)
        self.tasks.append(task)
        self.task_id_counter += 1  # Increment the task ID counter

    def delete_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                return True
        return False

    def generate_tasks(self): # ITERATOR, # GENERATOR
        for task in self.tasks:
            yield task

    def display_tasks(self):
        if not self.tasks:
            print("No tasks to display.")
            return

        # Determine the maximum width for each column
        max_widths = {
            "ID": 5,
            "Description": 20,
            "Priority": 10,
            "Due Date": 12
        }

        for task in self.tasks:
            # Update max_widths based on task details
            max_widths["ID"] = max(max_widths["ID"], len(str(task.task_id)))
            max_widths["Description"] = max(max_widths["Description"], len(task.description))
            max_widths["Priority"] = max(max_widths["Priority"], len(str(task.priority)))
            max_widths["Due Date"] = max(max_widths["Due Date"], len(task.due_date))

        # Display the tasks with adjusted column widths
        print("Tasks:")
        format_str = "{:<{id_width}} | {:<{desc_width}} | {:<{priority_width}} | {:<{due_date_width}}"
        print(format_str.format("ID", "Description", "Priority", "Due Date", 
                                id_width=max_widths["ID"] + 2,  # Adding 2 for padding
                                desc_width=max_widths["Description"] + 2,  # Adding 2 for padding
                                priority_width=max_widths["Priority"] + 2,  # Adding 2 for padding
                                due_date_width=max_widths["Due Date"] + 2))  # Adding 2 for padding
        print("-" * sum(max_widths.values()))

        for task in self.tasks:
            print(format_str.format(task.task_id, task.description, task.priority, task.due_date, 
                                    id_width=max_widths["ID"] + 2,  
                                    desc_width=max_widths["Description"] + 2,  
                                    priority_width=max_widths["Priority"] + 2,  
                                    due_date_width=max_widths["Due Date"] + 2))

    def sort_tasks(self, sort_option):
        if sort_option == 'priority':
            self.sorted_tasks = sorted(self.tasks, key=lambda x: x.priority, reverse=True)
        elif sort_option == 'due_date':
            self.sorted_tasks = sorted(self.tasks, key=lambda x: datetime.datetime.strptime(x.due_date, '%Y-%m-%d'))

    def display_sorted_tasks(self):
        if not self.sorted_tasks:
            print("No tasks to display.")
            return

        # Determine the maximum width for each column
        max_widths = {
            "ID": 5,
            "Description": 20,
            "Priority": 10,
            "Due Date": 12
        }

        for task in self.sorted_tasks:
            # Update max_widths based on task details
            max_widths["ID"] = max(max_widths["ID"], len(str(task.task_id)))
            max_widths["Description"] = max(max_widths["Description"], len(task.description))
            max_widths["Priority"] = max(max_widths["Priority"], len(str(task.priority)))
            max_widths["Due Date"] = max(max_widths["Due Date"], len(task.due_date))

        # Display the sorted tasks with adjusted column widths
        print("Sorted Tasks:")
        format_str = "{:<{id_width}} | {:<{desc_width}} | {:<{priority_width}} | {:<{due_date_width}}"
        print(format_str.format("ID", "Description", "Priority", "Due Date", 
                                id_width=max_widths["ID"] + 2,  # Adding 2 for padding
                                desc_width=max_widths["Description"] + 2,  # Adding 2 for padding
                                priority_width=max_widths["Priority"] + 2,  # Adding 2 for padding
                                due_date_width=max_widths["Due Date"] + 2))  # Adding 2 for padding
        print("-" * sum(max_widths.values()))

        for task in self.sorted_tasks:
            print(format_str.format(task.task_id, task.description, task.priority, task.due_date, 
                                    id_width=max_widths["ID"] + 2,  
                                    desc_width=max_widths["Description"] + 2,  
                                    priority_width=max_widths["Priority"] + 2,  
                                    due_date_width=max_widths["Due Date"] + 2))

    def save_tasks(self, filename, callback=None):
        with open(filename, 'w') as f:
            for task in self.tasks:
                f.write(f"{task.task_id},{task.description},{task.priority},{task.due_date}\n")
        if callback:
            callback()  # Call the callback function if provided

    def load_tasks(self, filename):
        if not os.path.exists(filename):
            print("Tasks file not found. Creating a new one.")
            return
        with open(filename, 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) != 4:
                    print("Error: Invalid data format in tasks file.")
                    continue
                task_id, description, priority, due_date = data
                self.add_task(description, priority, due_date)


# TaskManagerWithThreads Class
# This class extends TaskManager and introduces asynchronous task saving and loading using threading.
# __init__: Initializes the class.
# save_tasks_async: Asynchronously saves tasks to a file.
# load_tasks_async: Asynchronously loads tasks from a file.

class TaskManagerWithThreads(TaskManager):
    def __init__(self):
        super().__init__()

    def save_tasks_async(self, filename):
        def callback():
            print("Tasks saved to file.")
            time.sleep(1)  # Delay for 1 second
        save_thread = threading.Thread(target=self.save_tasks, args=(filename, callback))
        save_thread.start()

    def load_tasks_async(self, filename):
        load_thread = threading.Thread(target=self.load_tasks, args=(filename,))
        load_thread.start()


# Utility Functions
# These are helper functions used in the main program.

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    clear_screen()
    print("Welcome to the Task Manager!")
    print("Choose an option:")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Display Tasks")
    print("4. Sort Tasks")
    print("5. Save Tasks to File")
    print("6. Exit")

def get_valid_input(prompt, validation_func):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            print("Invalid input. Please try again.")

def validate_priority(priority):
    try:
        priority = int(priority)
        if priority < 1 or priority > 5:
            raise ValueError
        return priority
    except ValueError:
        return None

def validate_task_description(description):
    return any(char.isalpha() for char in description)

def validate_due_date(date_string):
    try:
        due_date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
        current_date = datetime.datetime.now().date()
        if due_date.date() >= current_date:
            return True
        else:
            return False
    except ValueError:
        return False


# Main Function
# The main function is where the program execution starts. 
# It initializes a TaskManagerWithThreads, loads tasks asynchronously, and enters a loop to display the menu and handle user choices.

def main():
    task_manager = TaskManagerWithThreads()  # Use TaskManagerWithThreads
    filename = "tasks.txt"
    task_manager.load_tasks_async(filename)  # Load tasks asynchronously

    while True:
        display_menu()
        choice = get_valid_input("Enter your choice: ", lambda x: x.isdigit() and 1 <= int(x) <= 6)

        if choice == '1':
            while True:
                description = input("Enter task description: ")
                if validate_task_description(description):
                    break
                else:
                    print("Task description must contain at least one non-integer character.")
            priority = get_valid_input("Enter task priority (1-5): ", lambda x: validate_priority(x))
            while True:
                due_date = input("Enter due date (YYYY-MM-DD): ")
                if validate_due_date(due_date):
                    break
                else:
                    print("Invalid date format or past date. Please enter a valid future date in YYYY-MM-DD format.")
            task_manager.add_task(description, priority, due_date)
            print("Task added successfully!")
            time.sleep(1)
        elif choice == '2':
            task_id = input("Enter task ID to delete: ")
            if not task_manager.delete_task(int(task_id)):
                print("Task not found.")
            else:
                print("Task deleted successfully!")
            time.sleep(1)
        elif choice == '3':
            task_manager.display_tasks()
            input("Press Enter to continue...")
        elif choice == '4':
            sort_option = get_valid_input("Sort tasks by (priority/due_date): ", lambda x: x in ['priority', 'due_date'])
            task_manager.sort_tasks(sort_option)
            task_manager.display_sorted_tasks()
            input("Press Enter to continue...")
        elif choice == '5':
            task_manager.save_tasks_async(filename)  # Save tasks asynchronously
        elif choice == '6':
            break

if __name__ == "__main__":
    main()
