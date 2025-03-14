import unittest
import json
import os
from datetime import datetime
from task_cli import add_task, update_task, delete_task, list_tasks, read_tasks, write_tasks, change_task_status

TASK_FILE = 'task_data.json'

class TaskCliTests(unittest.TestCase):

    def setUp(self):
        # Create a fresh task_data.json file before each test
        if os.path.exists(TASK_FILE):
            os.remove(TASK_FILE)
        write_tasks([])  # Write an empty task list to the file

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(TASK_FILE):
            os.remove(TASK_FILE)

    def test_add_task(self):
        # Test adding a new task
        add_task("New task")
        tasks = read_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['description'], "New task")
        self.assertEqual(tasks[0]['status'], "todo")
        self.assertTrue('id' in tasks[0])

    def test_add_duplicate_task(self):
        # Test adding a duplicate task (should not be added)
        add_task("New task")
        add_task("New task")  # Duplicate task
        tasks = read_tasks()
        self.assertEqual(len(tasks), 1)  # Only one task should be added
        self.assertEqual(tasks[0]['description'], "New task")

    def test_update_task(self):
        # Test updating a task
        add_task("Old task")
        task_id = read_tasks()[0]['id']
        update_task(task_id, "Updated task")
        tasks = read_tasks()
        updated_task = next((task for task in tasks if task['id'] == task_id), None)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task['description'], "Updated task")
        self.assertNotEqual(updated_task['updatedAt'], updated_task['createdAt'])

    def test_update_nonexistent_task(self):
        # Test updating a non-existent task
        update_task(999, "Updated task")
        # We should have an error message, but we're only testing the process
        tasks = read_tasks()
        self.assertEqual(len(tasks), 0)

    def test_delete_task(self):
        # Test deleting a task
        add_task("Task to be deleted")
        task_id = read_tasks()[0]['id']
        delete_task(task_id)
        tasks = read_tasks()
        self.assertEqual(len(tasks), 0)  # Task should be deleted

    def test_delete_nonexistent_task(self):
        # Test deleting a non-existent task
        delete_task(999)
        tasks = read_tasks()
        self.assertEqual(len(tasks), 0)  # No task should be deleted

    def test_change_task_status(self):
        # Test changing the status of a task
        add_task("Task with status")
        task_id = read_tasks()[0]['id']
        change_task_status(task_id, 'in-progress')
        tasks = read_tasks()
        updated_task = next((task for task in tasks if task['id'] == task_id), None)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task['status'], 'in-progress')

    def test_mark_done_task(self):
        # Test marking a task as 'done'
        add_task("Task to be done")
        task_id = read_tasks()[0]['id']
        change_task_status(task_id, 'done')
        tasks = read_tasks()
        updated_task = next((task for task in tasks if task['id'] == task_id), None)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task['status'], 'done')

    def test_list_tasks(self):
        # Test listing all tasks
        add_task("Task 1")
        add_task("Task 2")
        add_task("Task 3")
        tasks = list_tasks()
        self.assertGreater(len(tasks), 0)

    def test_list_filtered_tasks(self):
        # Test listing tasks by status filter
        add_task("Task 1")
        add_task("Task 2")
        add_task("Task 3")
        change_task_status(1, "done")
        tasks_done = list_tasks("done")
        self.assertEqual(len(tasks_done), 1)
        self.assertEqual(tasks_done[0]['status'], "done")

    def test_empty_task_list(self):
        # Test listing tasks when no tasks exist
        tasks = list_tasks()
        self.assertEqual(len(tasks), 0)

    def test_task_file_creation(self):
        # Test task file creation on first add
        tasks = read_tasks()
        self.assertEqual(len(tasks), 0)  # File should be empty initially
        add_task("Task to check file")
        tasks = read_tasks()
        self.assertEqual(len(tasks), 1)

if __name__ == '__main__':
    unittest.main()