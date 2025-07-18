# Fables

Repo for Fables project

Python 3.13.5

## UV Set Up

[Link to Documentation](https://astral.sh/blog/uv)

```bash
# Install
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify Install
uv

# Initialize Project
uv init

# Add Ruff
uv add ruff

# Verify Ruff Install
uv run ruff check
```

<br>

# Virtual Environment

```bash
# Create venv
uv venv

# Use venv
source .venv/bin/activate
```

<br>

# Docker Setup for Fables

## Problem

When running Docker containers that share volumes with your local filesystem, conflicts arise between:

- Python bytecode files (`__pycache__`, `.pyc` files)
- Virtual environment files (`.venv`)
- UV lock files and compiled dependencies

## Solution

### Option 1: Development-Only Container

```bash
# Run development container with selective volume mounting
docker compose -f docker-compose.dev.yml up --build -d

# With file watching
docker compose -f docker-compose.dev.yml up --build --watch
```

## Key Features

- **Isolated environments**: Container dependencies don't interfere with local `.venv`
- **Selective mounting**: Only source code is shared, not virtual environments
- **Database persistence**: PostgreSQL data persists between container restarts
- **Hot reload**: Changes to source code trigger automatic reloads
- **Clean separation**: Local and container environments remain independent

## Usage Commands

```bash
# Standard development
docker compose up --build

# Development with file watching
docker compose -f docker-compose.dev.yml up --build --watch

# Rebuild after dependency changes
docker compose build --no-cache

# Run Django commands in container
docker compose exec web uv run python manage.py makemigrations
docker compose exec web uv run python manage.py migrate
docker compose exec web uv run python manage.py createsuperuser

# Database access
docker compose exec db psql -U {{username}} -d fables
```

## Troubleshooting

1. **Virtual environment conflicts**: Ensure `.dockerignore` excludes `.venv/`
2. **Permission issues**: Use `docker compose down -v` to clean volumes
3. **Port conflicts**: Change port mappings in `docker-compose.yml`
4. **Database connection**: Ensure `DATABASES` settings point to `db` service

<br>

# PGAdmin Docker Setup

1. Ensure Docker container stack is running
   - Can use `docker compose down -v` to tear down existing stack
     - The `-v` flag removes the volumes, so the database will be recreated with the new credentials (from the `.env` file).
   - Can use `docker compose up -d` to recreate the stack
2. Go to http://localhost:5050
3. Login with `PGADMIN_DEFAULT_EMAIL` | `PGADMIN_DEFAULT_PASSWORD` environment variables
4. Click add server
   - Name:         `POSTGRES_DB` environment variable
   - Hostname:  `POSTGRES_HOST` environment variable
   - Port:            `POSTGRES_PORT` environment variable
   - Username: `POSTGRES_USER` environment variable
   - Password:  `POSTGRES_PASSWORD` environment variable
     - Toggled on 'Save Password'

<br>

# Set up Github Container Registry Access

You need to create a Personal Access Token (PAT) since GITHUB_TOKEN
is only available inside GitHub Actions, not for local development.

Create a Personal Access Token:

1. Go to GitHub Settings: - Click your profile picture → Settings → Developer settings →
   Personal access tokens → Tokens (classic)
2. Generate New Token:
   - Click "Generate new token (classic)"
   - Give it a name like "Docker Registry Access"
   - Set expiration (recommended: 90 days or 1 year)
3. Select Permissions:
   - Check: read:packages (to pull images)
   - Optionally: write:packages (if you want to push from local)
4. Copy the Token

Login directly (paste token when prompted for password):

```bash
# store your PAT in the .env
docker login ghcr.io -u YOUR_GITHUB_USERNAME
```

<br>

# Running Django Tests

We have unit/integration tests for each module. You will be able to run tests within the docker container using a command like below:

```bash
# replace campaigns with whichever app you want to run tests against
docker compose exec web uv run python manage.py test campaigns -v 2
```

Django tests use a separate test database that's
automatically created and destroyed for each test run. Here's
how it works:

1. Test Database Creation: Django creates a temporary test
   database
2. Isolated Tests: Each test runs in a transaction that's
   rolled back after completion
3. Clean Slate: Every test method starts with a fresh, empty
   database
4. Test Database Destruction: After all tests finish, Django
   destroys the test database

This isolation is a feature - it ensures tests are repeatable
and don't interfere with your application data.
