import json
import os

FILE_NAME = "tasks.json"

# ---------------------------
# Load Tasks
# ---------------------------
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# ---------------------------
# Save Tasks
# ---------------------------
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# ---------------------------
# Add Task
# ---------------------------
def add_task(tasks):
    task = input("Enter Task: ")
    priority = input("Priority (High/Medium/Low): ")
    due = input("Due Date (DD-MM-YYYY): ")

    tasks.append({
        "task": task,
        "priority": priority,
        "due": due,
        "completed": False
    })

    save_tasks(tasks)
    print("Task Added Successfully!")

# ---------------------------
# View Tasks
# ---------------------------
def view_tasks(tasks):

    if not tasks:
        print("\nNo Tasks Found.\n")
        return

    print("\n========== TO DO LIST ==========\n")

    for i, t in enumerate(tasks, start=1):

        status = "Done" if t["completed"] else "Pending"

        print(f"{i}. {t['task']}")
        print(f"   Priority : {t['priority']}")
        print(f"   Due Date : {t['due']}")
        print(f"   Status   : {status}")
        print()

# ---------------------------
# Complete Task
# ---------------------------
def complete_task(tasks):

    view_tasks(tasks)

    try:
        num = int(input("Enter Task Number: "))
        tasks[num-1]["completed"] = True
        save_tasks(tasks)
        print("Task Completed.")
    except:
        print("Invalid Input.")

# ---------------------------
# Delete Task
# ---------------------------
def delete_task(tasks):

    view_tasks(tasks)

    try:
        num = int(input("Enter Task Number: "))
        tasks.pop(num-1)
        save_tasks(tasks)
        print("Task Deleted.")
    except:
        print("Invalid Input.")

# ---------------------------
# Edit Task
# ---------------------------
def edit_task(tasks):

    view_tasks(tasks)

    try:
        num = int(input("Enter Task Number: "))

        tasks[num-1]["task"] = input("New Task: ")
        tasks[num-1]["priority"] = input("Priority: ")
        tasks[num-1]["due"] = input("Due Date: ")

        save_tasks(tasks)
        print("Task Updated.")

    except:
        print("Invalid Input.")

# ---------------------------
# Search Task
# ---------------------------
def search_task(tasks):

    keyword = input("Enter Keyword: ").lower()

    found = False

    for i, t in enumerate(tasks, start=1):

        if keyword in t["task"].lower():

            print(f"\n{i}. {t['task']}")
            print("Priority:", t["priority"])
            print("Due:", t["due"])
            print("Completed:", t["completed"])
            found = True

    if not found:
        print("Task Not Found.")

# ---------------------------
# Statistics
# ---------------------------
def statistics(tasks):

    total = len(tasks)
    completed = sum(t["completed"] for t in tasks)
    pending = total - completed

    print("\n------ Statistics ------")
    print("Total Tasks :", total)
    print("Completed :", completed)
    print("Pending :", pending)

# ---------------------------
# Main Program
# ---------------------------
tasks = load_tasks()

while True:

    print("""
==============================
      TO DO LIST MENU
==============================

1. Add Task
2. View Tasks
3. Complete Task
4. Delete Task
5. Edit Task
6. Search Task
7. Statistics
8. Exit

==============================
""")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_task(tasks)

    elif choice == "2":
        view_tasks(tasks)

    elif choice == "3":
        complete_task(tasks)

    elif choice == "4":
        delete_task(tasks)

    elif choice == "5":
        edit_task(tasks)

    elif choice == "6":
        search_task(tasks)

    elif choice == "7":
        statistics(tasks)

    elif choice == "8":
        print("Thank You!")
        break

    else:
        print("Invalid Choice.")