# Fables

Repo for Fables project

Python 3.13.5

## UV Set Up

[Link to Documentation](https://astral.sh/blog/uv)

1. Install                    `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Verify install          `uv`
3. Initialize project    `uv init`
4. Add Ruff                `uv add ruff`
5. Verify Ruff install  `uv run ruff check`

# Virtual Environment

1. Create virtual environment `uv venv`
2. Use virtual environment `source .venv/bin/activate`

## Run Docker

1. Ensure Docker is available in local env and use command `docker compose up -d`
   - Django app will be available at http://localhost:8000 and PostgreSQL at
     http://localhost:5433
     - Note: there is no web interface for Postgres, you can validate it is running using a command like:
       - `docker compose exec web uv run python manage.py dbshell --help`
       - `docker compose exec db psql -U fables_user -d fables`
         - direct connection to the db container
2. To stop the containers use `docker compose down`

### Run migrations (in separate terminal)

`docker compose exec web uv run python manage.py migrate`

### Create superuser (optional)

`docker compose exec web uv run python manage.py createsuperuser`

## PGAdmin Docker Setup

1. Ensure Docker container stack is running
   - Can use `docker-compose down -v` to tear down existing stack
     - The `-v` flag removes the volumes, so the database will be recreated with the new credentials (from the `.env` file).
   - Can use `docker-compose up -d` to recreate the stack
2. Go to http://localhost:5050
3. Login with `PGADMIN_DEFAULT_EMAIL` | `PGADMIN_DEFAULT_PASSWORD` environment variables
4. Click add server
   - Name:         `POSTGRES_DB` environment variable
   - Hostname:  `POSTGRES_HOST` environment variable
   - Port:            `POSTGRES_PORT` environment variable
   - Username: `POSTGRES_USER` environment variable
   - Password:  `POSTGRES_PASSWORD` environment variable
     - Toggled on 'Save Password'
