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

### Option 1: Standard Docker Compose (Recommended)
```bash
# Build and run with PostgreSQL database
docker compose up --build -d

# Stop services
docker compose down

# Clean up volumes
docker compose down -v
```

### Option 2: Development-Only Container
```bash
# Run development container with selective volume mounting
docker compose -f docker-compose.dev.yml up --build -d

# With file watching
docker compose -f docker-compose.dev.yml up --build --watch
```

### Option 3: Local Development + Docker Database
```bash
# Run only PostgreSQL in Docker
docker compose up --no-deps db

# Then run Django locally
uv run python manage.py runserver
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
