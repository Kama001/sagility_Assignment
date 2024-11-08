import sys
import os
from pathlib import Path

# Add the root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)  # Create a TestClient to send requests to the app

def test_create_task():
    """Test the endpoint to create a new task."""
    response = client.post("/tasks/", json={"title": "Buy groceries", "description": "Milk, eggs, bread"})
    assert response.status_code == 200
    assert response.json()["title"] == "Buy groceries"
    assert response.json()["description"] == "Milk, eggs, bread"
    assert response.json()["completed"] is False
    assert "id" in response.json()  # Ensure task has an ID

def test_get_all_tasks():
    """Test the endpoint to get all tasks."""
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Response should be a list
    assert len(response.json()) > 0  # Ensure there is at least one task

def test_get_task_by_id():
    """Test the endpoint to retrieve a task by ID."""
    # First, create a task
    create_response = client.post(
        "/tasks/", json={"title": "Buy groceries", "description": "Milk, eggs, bread"}
    )
    task_id = create_response.json()["id"]
    
    # Now, retrieve the task by ID
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id  # Ensure correct task is returned
    assert response.json()["title"] == "Buy groceries"

def test_update_task():
    """Test the endpoint to update an existing task."""
    # First, create a task
    create_response = client.post(
        "/tasks/", json={"title": "Buy groceries", "description": "Milk, eggs, bread"}
    )
    task_id = create_response.json()["id"]
    
    # Update the task
    updated_data = {"title": "Buy groceries and more", "completed": True}
    update_response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Buy groceries and more"
    assert update_response.json()["completed"] is True

def test_delete_task():
    """Test the endpoint to delete a task."""
    # First, create a task
    create_response = client.post(
        "/tasks/", json={"title": "Buy groceries", "description": "Milk, eggs, bread"}
    )
    task_id = create_response.json()["id"]
    
    # Now, delete the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == task_id  # Ensure the correct task is deleted

    # Ensure task is deleted by trying to retrieve it
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404  # Task should not be found

def test_create_task_missing_field():
    """Test creating a task with a missing required field."""
    response = client.post(
        "/tasks/", json={"description": "Milk, eggs, bread"}  # Missing 'title'
    )
    assert response.status_code == 422  # Unprocessable Entity

def test_get_task_not_found():
    """Test getting a non-existent task."""
    response = client.get("/tasks/999")  # Task ID 999 doesn't exist
    assert response.status_code == 404  # Should return a 404 error
    assert "error" in response.json()  # Should return an error message
