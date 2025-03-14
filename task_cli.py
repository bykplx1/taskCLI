import json
import os
import sys
from datetime import datetime

TASK_FILE = 'task_data.json'

def read_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    with open(TASK_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_tasks(tasks): 
    with open(TASK_FILE, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = read_tasks()
    if any(task['description'] == description for task in tasks):
        print("Task with this description already exists. Please add a unique task.")
        return
    task_id = 1 if not tasks else tasks[-1]['id'] + 1
    task = {
        'id': task_id,
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        'updatedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
    }
    tasks.append(task)
    write_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

def update_task(task_id, new_description):
    tasks = read_tasks()
    task = next((task for task in tasks if task['id'] == int(task_id)), None)
    if task:
        task['description'] = new_description
        task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        write_tasks(tasks)
        print(f"Task {task_id} updated successfully.")
    else:
        print(f"Task {task_id} not found.")

def delete_task(task_id):
    tasks = read_tasks()
    tasks = [task for task in tasks if task['id'] != int(task_id)]
    write_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")

def change_task_status(task_id, new_status):
    tasks = read_tasks()
    task = next((task for task in tasks if task['id'] == int(task_id)), None)
    if task:
        task['status'] = new_status
        task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        write_tasks(tasks)
        print(f"Task {task_id} status changed to {new_status}.")
    else:
        print(f"Task {task_id} not found.")

def list_tasks(status=None):
    tasks = read_tasks()
    if status:
        tasks = [task for task in tasks if task['status'] == status]

    if tasks:
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, CreatedAt: {task['createdAt']}, UpdatedAt: {task['updatedAt']}")
        return tasks
    else:
        print("No tasks found.")
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == 'add' and len(sys.argv) == 3:
        add_task(sys.argv[2])
    elif command == 'update' and len(sys.argv) == 4:
        update_task(sys.argv[2], sys.argv[3])
    elif command == 'delete' and len(sys.argv) == 3:
        delete_task(sys.argv[2])
    elif command == 'mark-in-progress' and len(sys.argv) == 3:
        change_task_status(sys.argv[2], 'in-progress')
    elif command == 'mark-done' and len(sys.argv) == 3:
        change_task_status(sys.argv[2], 'done')
    elif command == 'list' and len(sys.argv) == 2:
        list_tasks()
    elif command == 'list' and len(sys.argv) == 3:
        list_tasks(sys.argv[2])
    else:
        print("Invalid command or arguments.")
        print("Usage: task-cli <command> [arguments]")


if __name__ == '__main__':
    main()