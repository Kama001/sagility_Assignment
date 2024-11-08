"""
Main FastAPI application.

This file contains the FastAPI app and the necessary CRUD routes to manage tasks.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# In-memory task list to simulate a database
tasks = []

class Task(BaseModel):
    """
    Represents a task with a title, description, and completion status.
    """
    title: str
    description: str = None
    completed: bool = False

@app.post("/tasks/")
def create_task(task: Task):
    """
    Create a new task.

    Args:
        task (Task): The task to be created.

    Returns:
        dict: The created task with an 'id' field.
    """
    task_id = max((task["id"] for task in tasks), default=0) + 1
    task_data = task.dict()
    task_data["id"] = task_id
    tasks.append(task_data)
    return task_data

@app.get("/tasks/")
def get_tasks():
    """
    Get all tasks.

    Returns:
        List[dict]: A list of all tasks.
    """
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """
    Get a specific task by its ID.

    Args:
        task_id (int): The ID of the task to retrieve.

    Returns:
        dict: The task data.
    """
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return {"error": "Task not found"}, 404
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    """
    Update a specific task by its ID.

    Args:
        task_id (int): The ID of the task to update.
        task (Task): The updated task data.

    Returns:
        dict: The updated task data.
    """
    existing_task = next((task for task in tasks if task["id"] == task_id), None)
    if existing_task is None:
        return {"error": "Task not found"}, 404
    existing_task.update(task.dict())
    return existing_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """
    Delete a specific task by its ID.

    Args:
        task_id (int): The ID of the task to delete.

    Returns:
        dict: The deleted task data.
    """
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return {"error": "Task not found"}, 404
    tasks.remove(task)
    return task
