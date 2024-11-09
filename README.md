# Project Title

A CI/CD pipeline to deploy a TODO-app written using FASTAPI

## Description

This app is a basic TODO-app written using FASTAPI. It has basic apis to create, delete, update, get tasks.
A simple test file is there to test the application.
A CI pipeline is setup to check for liniting errors, test the application then build and push to Docker
A CD pipeline is setup to do the deployment of the application to the self-hosted runner having minikube already installed.

## Table of Contents (Optional)

- [Installation](#installation)
- [Usage](#usage)

## Installation

### Prerequisites
- To push docker image to docker hub in CI stage, keep the dockerhub username and password in secrets and variables section of the repo. To do that
- Goto Settings of ur repo -> Select Actions on left panel -> select actions -> add secrets to secrets section
- The application will be deployed on a self hosted runner. So register a runner prior to deployment.
- Make sure runner is having minikube and helm installed.
- To install minikube --> https://minikube.sigs.k8s.io/docs/start/
- To install helm --> https://helm.sh/docs/intro/install/
- To register runner
- Goto Settings of ur repo -> Select Actions on left panel -> Choose runners -> Select self-hosted runner -> follow the instruction given

### Steps to Install
1. Clone the repository:
     https://github.com/Kama001/sagility_Assignment.git
2. Make required changes and push.
3. A CI job will be automatically triggered.
4. After CI job completes CD job will be triggered to do the deployment

## Usage
To interact with the application use following api calls.
Get minikube IP and use port defined in values.yaml of Helm

### Create a Task (POST /tasks/):
curl -X 'POST' \
http://minikubeIP:port/tasks/ \
-H 'Content-Type: application/json' \
-d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
### Expected Response (example):
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}

### Get All Tasks (GET /tasks/):
curl -X 'GET' 'http://minikubeIP:port/tasks/'

### Expected Response (example):
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
  }
}

### Get a Specific Task (GET /tasks/{task_id}):
curl -X 'GET' 'http://minikubeIP:port/tasks/1'

### Expected Response (example):
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}

### Update a Task (PUT /tasks/{task_id}):
curl -X 'PUT' \
  'http://minikubeIP:port/tasks/1' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Buy groceries and more",
    "completed": true
  }'
### Expected Response (example):
{
  "id": 1,
  "title": "Buy groceries and more",
  "description": "Milk, eggs, bread",
  "completed": true
}

### Delete a Task (DELETE /tasks/{task_id}):
curl -X 'DELETE' 'http://minikubeIP:port/tasks/1'
### Expected Response (example):
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}




