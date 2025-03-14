---

# Task CLI Application

This is a simple command-line tool for managing tasks. You can add, update, delete, and change the status of tasks, all through commands in your terminal.

## Table of Contents
- [About](#about)
- [Setup](#setup)
- [Commands](#commands)
- [Testing](#testing)

## About

The `Task CLI` application is a Python-based command-line tool designed to help users manage tasks. It allows you to:

- **Add** new tasks
- **Update** existing tasks
- **Delete** tasks
- **Change task status** (e.g., mark tasks as done or in-progress)
- **List tasks** based on their status

## Setup

To run the Task CLI application, you'll need to set up your environment and ensure Python is installed.

### Prerequisites

- Python 3.7 or higher
- `pip` package manager (comes with Python)
- Access to the command line or terminal

### 1. Install Python (if not already installed)

- **Windows**: [Download Python](https://www.python.org/downloads/)
- **macOS**: Use Homebrew or download from [Python's official website](https://www.python.org/downloads/).
- **Linux**: Install via package manager, e.g., `sudo apt install python3`.

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/task-cli.git
cd task-cli
```

### 3. Set up PATH to run the app globally (Optional)

To be able to run the app from anywhere in the terminal, add the project directory to your system's `PATH` variable.

#### Windows:
1. Press `Windows + R`, then type `sysdm.cpl` and press Enter.
2. Click on the **Advanced** tab, then **Environment Variables**.
3. Under **System Variables**, select **Path** and click **Edit**.
4. Click **New** and add the path to your project directory (e.g., `C:\path\to\task-cli`).
5. Click **OK** and restart your terminal.

#### macOS/Linux:
1. Open the terminal.
2. Add the project directory to your `PATH` by running:
   ```bash
   echo 'export PATH="$PATH:/path/to/task-cli"' >> ~/.bash_profile
   source ~/.bash_profile
   ```

Now you should be able to run `task-cli` from any directory in the terminal.

## Commands

### 1. Add a Task

To add a new task:

```bash
task-cli add "Task description"
```

Example:

```bash
task-cli add "Buy groceries"
```

### 2. Update a Task

To update the description of an existing task:

```bash
task-cli update <task-id> "New description"
```

Example:

```bash
task-cli update 1 "Buy groceries and cook dinner"
```

### 3. Delete a Task

To delete a task by its ID:

```bash
task-cli delete <task-id>
```

Example:

```bash
task-cli delete 1
```

### 4. Change Task Status

To mark a task as "in-progress":

```bash
task-cli mark-in-progress <task-id>
```

To mark a task as "done":

```bash
task-cli mark-done <task-id>
```

Example:

```bash
task-cli mark-in-progress 1
task-cli mark-done 2
```

### 5. List Tasks

To list all tasks:

```bash
task-cli list
```

To list tasks filtered by status (e.g., "done"):

```bash
task-cli list done
```

Example:

```bash
task-cli list
task-cli list done
```

## Testing

This project uses Python’s `unittest` module for testing.

### 1. Running Tests

To run all tests, use the following command in the terminal:

```bash
python test_task_cli.py
```

### 2. Running Tests via Batch File (Windows)

If you're on Windows, you can use the provided `.bat` file to run the tests:

```bash
run_tests.bat
```

This will run all the tests and show you a summary at the end of the output.

### 3. Viewing Test Results

After running the tests, you'll get a test summary with details on whether the tests passed or failed. The output will also show the errors or failures for failed tests.

Example output:
```
Total Tests Run: 12
Errors: 0
Failures: 0
✅ ALL TESTS PASSED! ✅
```
---
