import unittest
from unittest.mock import patch, mock_open
import json
from task_cli import add_task, load_tasks, save_tasks

class TestTaskCLI(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='[]')  # Mock file opening and reading an empty list
    def test_add_task_new_task(self, mock_file):
        # Test adding a new task
        description = "Test Task"
        
        # Run add_task function (it will try to load tasks, add a task, and save tasks)
        add_task(description)
        
        # Check that open() was called to write to the file
        mock_file.assert_called_once_with('task_data.json', 'w')
        
        # Check the data written to the file
        handle = mock_file()
        written_data = handle.write.call_args[0][0]  # Get the data passed to the write function
        tasks = json.loads(written_data)  # Parse the written data as JSON
        
        # Check that the task was added
        self.assertEqual(len(tasks), 1)  # One task should be in the list
        self.assertEqual(tasks[0]['description'], description)  # Task description should match

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "description": "Test Task", "status": "todo", "createdAt": "2025-03-14", "updatedAt": "2025-03-14"}
    ]))  # Mock file reading with an existing task
    def test_add_task_duplicate(self, mock_file):
        # Test trying to add a duplicate task
        description = "Test Task"
        
        # Run add_task function
        add_task(description)
        
        # Ensure the task is not added (file should not be modified)
        mock_file.assert_not_called_with('task_data.json', 'w')  # No writing to file should occur

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "description": "Test Task 1", "status": "todo", "createdAt": "2025-03-14", "updatedAt": "2025-03-14"}
    ]))
    def test_add_task_new_unique_task(self, mock_file):
        # Test adding a new task with a unique description
        description = "Test Task 2"
        
        # Run add_task function
        add_task(description)
        
        # Check that open() was called to write to the file
        mock_file.assert_called_once_with('task_data.json', 'w')
        
        # Check the data written to the file
        handle = mock_file()
        written_data = handle.write.call_args[0][0]
        tasks = json.loads(written_data)
        
        # Check that the new task was added
        self.assertEqual(len(tasks), 2)  # Total of 2 tasks now
        self.assertEqual(tasks[1]['description'], description)  # New task description should match

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "description": "Test Task 1", "status": "todo", "createdAt": "2025-03-14", "updatedAt": "2025-03-14"}
    ]))
    def test_load_tasks(self, mock_file):
        # Test loading tasks from the file
        tasks = load_tasks()
        
        # Verify that tasks are correctly loaded
        self.assertEqual(len(tasks), 1)  # One task in the file
        self.assertEqual(tasks[0]['description'], "Test Task 1")  # Description should match

    @patch('builtins.open', new_callable=mock_open)
    def test_save_tasks(self, mock_file):
        # Test saving tasks to the file
        tasks = [
            {"id": 1, "description": "Test Task", "status": "todo", "createdAt": "2025-03-14", "updatedAt": "2025-03-14"}
        ]
        
        save_tasks(tasks)
        
        # Ensure that the correct data is written to the file
        mock_file.assert_called_once_with('task_data.json', 'w')
        handle = mock_file()
        written_data = handle.write.call_args[0][0]
        written_tasks = json.loads(written_data)  # Load the written JSON data
        self.assertEqual(len(written_tasks), 1)  # Only one task should be in the list

if __name__ == '__main__':
    unittest.main()