import unittest
import json
import os
from datetime import datetime
import sys
from io import StringIO
from task_cli import add_task, update_task, delete_task, list_tasks, read_tasks, write_tasks, change_task_status

TASK_FILE = 'task_data.json'

class TaskCliTests(unittest.TestCase):

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output
        if os.path.exists(TASK_FILE):
            os.remove(TASK_FILE)
        write_tasks([])

    def tearDown(self):
        sys.stdout = sys.__stdout__
        if os.path.exists(TASK_FILE):
            os.remove(TASK_FILE)

    def test_add_task(self):
        add_task("New task")
        tasks = read_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['description'], "New task")
        self.assertEqual(tasks[0]['status'], "todo")
        self.assertTrue('id' in tasks[0])

    def test_add_duplicate_task(self):
        add_task("New task")
        add_task("New task")
        tasks = read_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['description'], "New task")

    def test_update_task(self):
        add_task("Old task")
        task_id = read_tasks()[0]['id']
        update_task(task_id, "Updated task")
        tasks = read_tasks()
        updated_task = next((task for task in tasks if task['id'] == task_id), None)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task['description'], "Updated task")
        self.assertNotEqual(updated_task['updatedAt'], updated_task['createdAt'])

    def test_update_nonexistent_task(self):
        update_task(999, "Updated task")
        tasks = read_tasks()
        self.assertEqual(len(tasks), 0)

    def test_delete_task(self):
        add_task("Task to be deleted")
        task_id = read_tasks()[0]['id']
        delete_task(task_id)
        tasks = read_tasks()
        self.assertEqual(len(tasks), 0)

    def test_delete_nonexistent_task(self):
        delete_task(999)
        tasks = read_tasks()
        self.assertEqual(len(tasks), 0)

    def test_change_task_status(self):
        add_task("Task with status")
        task_id = read_tasks()[0]['id']
        change_task_status(task_id, 'in-progress')
        tasks = read_tasks()
        updated_task = next((task for task in tasks if task['id'] == task_id), None)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task['status'], 'in-progress')

    def test_mark_done_task(self):
        add_task("Task to be done")
        task_id = read_tasks()[0]['id']
        change_task_status(task_id, 'done')
        tasks = read_tasks()
        updated_task = next((task for task in tasks if task['id'] == task_id), None)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task['status'], 'done')

    def test_list_tasks(self):
        add_task("Task 1")
        add_task("Task 2")
        add_task("Task 3")
        tasks = list_tasks()
        self.assertGreater(len(tasks), 0)

    def test_list_filtered_tasks(self):
        add_task("Task 1")
        add_task("Task 2")
        add_task("Task 3")
        change_task_status(1, "done")
        tasks_done = list_tasks("done")
        self.assertEqual(len(tasks_done), 1)
        self.assertEqual(tasks_done[0]['status'], "done")

    def test_empty_task_list(self):
        tasks = list_tasks()
        self.assertEqual(len(tasks), 0)

    def test_task_file_creation(self):
        tasks = read_tasks()
        self.assertEqual(len(tasks), 0)
        add_task("Task to check file")
        tasks = read_tasks()
        self.assertEqual(len(tasks), 1)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover(".")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print the custom report
    print("\n" + "="*50)
    print("TEST REPORT SUMMARY")
    print("="*50)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED! ✅")
    else:
        print("\n❌ SOME TESTS FAILED ❌")