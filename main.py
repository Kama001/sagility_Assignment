from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Create FastAPI app
app = FastAPI()

# In-memory storage for tasks (acting as a temporary "database")
tasks = []

# Pydantic models for validation and serialization
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    completed: Optional[bool] = None

class Task(TaskBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True

# Utility to get the next task ID
def get_next_task_id():
    return max([task.id for task in tasks], default=0) + 1

# Endpoint to create a task
@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    task_id = get_next_task_id()
    new_task = Task(id=task_id, title=task.title, description=task.description, completed=False)
    tasks.append(new_task)
    return new_task

# Endpoint to get all tasks
@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks

# Endpoint to get a single task by ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Endpoint to update a task
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_update.title:
        task.title = task_update.title
    if task_update.description:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed

    return task

# Endpoint to delete a task
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks.remove(task)
    return task
