#!/bin/bash

# ==== START DATABASE CONTAINERS ONLY ====
echo "Starting database and pgadmin containers..."
docker compose -f docker-compose.dev.yml up -d db pgadmin

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 5

# ==== AUTO-DETECT CONTAINERS ====
DB_CONTAINER=$(docker compose -f docker-compose.dev.yml ps --format '{{.Name}}' | grep -i db)
PGADMIN_CONTAINER=$(docker compose -f docker-compose.dev.yml ps --format '{{.Name}}' | grep -i pgadmin)

if [ -z "$DB_CONTAINER" ]; then
    echo "Could not detect Postgres container."
    echo "Available containers:"
    docker compose -f docker-compose.dev.yml ps
    exit 1
fi

# Set web container name (will be created later)
WEB_CONTAINER="fables-web-1"

# ==== AUTO-DETECT POSTGRES USER ====
DB_USER=$(docker exec -i "$DB_CONTAINER" env | grep POSTGRES_USER | cut -d '=' -f2)
if [ -z "$DB_USER" ]; then
    echo "Could not detect POSTGRES_USER from $DB_CONTAINER"
    exit 1
fi

# ==== LOAD ENVIRONMENT VARIABLES ====
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Warning: .env file not found, using default values"
fi

# ==== CONFIGURE THESE ====
DB_NAME="${POSTGRES_DB:-fables}"                                   # Database name from .env
SUPERUSER_EMAIL="${PGADMIN_DEFAULT_EMAIL:-admin@example.com}"      # Superuser email from .env
SUPERUSER_USERNAME="admin"                                         # Superuser username (default)
SUPERUSER_PASSWORD="${PGADMIN_DEFAULT_PASSWORD:-adminpass123}"     # Superuser password from .env
APPS=("accounts" "campaigns")                                      # Local apps to reset migrations for
# ==========================

echo "Using Postgres container: $DB_CONTAINER"
echo "Web container will be: $WEB_CONTAINER"
if [ -n "$PGADMIN_CONTAINER" ]; then
    echo "Using PgAdmin container: $PGADMIN_CONTAINER"
fi
echo "Postgres user: $DB_USER"
echo "Database name: $DB_NAME"

# Final database readiness check
until docker exec "$DB_CONTAINER" pg_isready -U "$DB_USER" > /dev/null 2>&1; do
    echo "Database not ready yet, waiting..."
    sleep 2
done
echo "Database is confirmed ready!"

# ==== 1. Drop and recreate the database ====
echo "Terminating active connections to database..."
docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d postgres -c "
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE datname = '$DB_NAME' AND pid <> pg_backend_pid();
"

echo "Dropping and recreating database..."
docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;" || echo "Drop database failed or database didn't exist"
docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;" || echo "Create database failed"

echo "Verifying database was recreated..."
docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d postgres -c "SELECT datname FROM pg_database WHERE datname = '$DB_NAME';"

# ==== 2. Start web container for Django operations ====
echo "Starting web container for Django operations..."
docker compose -f docker-compose.dev.yml start web

# Wait for web container to be ready
echo "Waiting for web container to be ready..."
sleep 5

# ==== 3. Delete migrations for specific apps ====
echo "Removing migrations for apps: ${APPS[*]}..."
for app in "${APPS[@]}"; do
    docker exec -i "$WEB_CONTAINER" sh -c "find $app/migrations -type f -not -name '__init__.py' -delete || true"
done

# ==== 4. Make migrations for all apps ====
echo "Making migrations for all apps..."
docker exec -i "$WEB_CONTAINER" uv run python manage.py makemigrations
echo "Making migrations for specific apps..."
for app in "${APPS[@]}"; do
    docker exec -i "$WEB_CONTAINER" uv run python manage.py makemigrations "$app"
done

# ==== 5. Apply migrations ====
echo "Applying migrations..."
docker exec -i "$WEB_CONTAINER" uv run python manage.py migrate

# ==== 6. Create superuser ====
echo "Creating superuser..."
docker exec -i "$WEB_CONTAINER" uv run python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="$SUPERUSER_EMAIL").exists():
    User.objects.create_superuser(
        email="$SUPERUSER_EMAIL",
        username="$SUPERUSER_USERNAME",
        password="$SUPERUSER_PASSWORD"
    )
    print("Superuser created: $SUPERUSER_EMAIL / $SUPERUSER_PASSWORD")
else:
    print("Superuser already exists.")
EOF

# ==== 7. Run seed_all command ====
echo "Running seed_all command with force flag..."
docker exec -i "$WEB_CONTAINER" uv run python manage.py seed_all --force

# ==== 8. Final restart for clean state ====
echo "Database reset complete!"
echo "Restarting web container..."
docker compose -f docker-compose.dev.yml restart web

echo "Setup complete!"
echo "Access Django admin at: http://127.0.0.1:8000/admin/"
echo "Login with: $SUPERUSER_EMAIL / $SUPERUSER_PASSWORD"
if [ -n "$PGADMIN_CONTAINER" ]; then
    echo "Access PgAdmin at: http://127.0.0.1:5050/"
    echo "PgAdmin login available with environment variables"
fi
echo "Press CTRL+C to stop all services."