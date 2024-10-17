# FastAPI Project - Backend

## Requirements

- [Docker](https://www.docker.com/).
- [Poetry](https://python-poetry.org/) for Python package and environment management.

## Local Development

- Start the stack with Docker Compose:

```bash
docker compose up -d
```

- Now you can open your browser and interact with these URLs:

Backend, JSON based web API based on OpenAPI: http://localhost:8080/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8080/docs

## Backend local development, additional details

### General workflow

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

From `./app/` you can install all the dependencies with:

```console
$ poetry install
```

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```

Make sure your editor is using the correct Python virtual environment.

Modify or add SQLModel models for data and SQL tables in `./backend/app/models/`, API endpoints in `./backend/app/api/`, CRUD (Create, Read, Update, Delete) utils in `./backend/app/crud.py`.

### VS Code

There are already configurations in place to run the backend through the VS Code debugger, so that you can use breakpoints, pause and explore variables, etc.

The setup is also already configured so you can run the tests through the VS Code Python tests tab.

### Deployment

```bash
docker build --tag dodo-be .
az containerapp up --resource-group dodo-be-rg --name dodo-be --ingress external --target-port 8000 --source .
```
