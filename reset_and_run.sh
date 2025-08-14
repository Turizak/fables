#!/bin/bash

# ==== AUTO-DETECT CONTAINERS ====
DB_CONTAINER=$(docker ps --format '{{.Names}} {{.Image}}' | grep -i postgres | awk '{print $1}')
WEB_CONTAINER=$(docker ps --format '{{.Names}} {{.Image}}' | grep -i fables | grep -i web | awk '{print $1}')

if [ -z "$DB_CONTAINER" ] || [ -z "$WEB_CONTAINER" ]; then
    echo "❌ Could not detect Postgres or Django container."
    echo "   Make sure both are running with: docker ps"
    exit 1
fi

# ==== AUTO-DETECT POSTGRES USER ====
DB_USER=$(docker exec -i "$DB_CONTAINER" env | grep POSTGRES_USER | cut -d '=' -f2)
if [ -z "$DB_USER" ]; then
    echo "❌ Could not detect POSTGRES_USER from $DB_CONTAINER"
    exit 1
fi

# ==== CONFIGURE THESE ====
DB_NAME="fables"                   # Database name
SUPERUSER_EMAIL="admin@example.com"      # Superuser email
SUPERUSER_USERNAME="admin"               # Superuser username
SUPERUSER_PASSWORD="adminpass123"        # Superuser password
APPS=("accounts" "campaigns")            # Local apps to reset migrations for
# ==========================

echo "📦 Using Postgres container: $DB_CONTAINER"
echo "📦 Using Django container: $WEB_CONTAINER"
echo "👤 Postgres user: $DB_USER"
echo "🗄  Database name: $DB_NAME"

# ==== 1. Delete migrations for specific apps ====
echo "🧹 Removing migrations for apps: ${APPS[*]}..."
for app in "${APPS[@]}"; do
    docker exec -i "$WEB_CONTAINER" sh -c "find $app/migrations -type f -not -name '__init__.py' -delete || true"
done

# ==== 2. Drop and recreate the database ====
echo "🚀 Dropping and recreating database..."
docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;"

# ==== 3. Make migrations for all apps ====
echo "📦 Making migrations..."
docker exec -i "$WEB_CONTAINER" uv run python manage.py makemigrations

# ==== 4. Apply migrations ====
echo "⚙️ Applying migrations..."
docker exec -i "$WEB_CONTAINER" uv run python manage.py migrate

# ==== 5. Create superuser ====
echo "👑 Creating superuser..."
docker exec -i "$WEB_CONTAINER" uv run python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="$SUPERUSER_EMAIL").exists():
    User.objects.create_superuser(
        email="$SUPERUSER_EMAIL",
        username="$SUPERUSER_USERNAME",
        password="$SUPERUSER_PASSWORD"
    )
    print("✅ Superuser created: $SUPERUSER_EMAIL / $SUPERUSER_PASSWORD")
else:
    print("ℹ️ Superuser already exists.")
EOF

# ==== 6. Start the dev server ====
echo "🎉 Database reset complete!"
echo "🌐 Starting Django development server..."
echo "💡 Access admin at: http://127.0.0.1:8000/admin/"
echo "   Login with: $SUPERUSER_EMAIL / $SUPERUSER_PASSWORD"
echo "   Press CTRL+C to stop the server."

docker exec -it "$WEB_CONTAINER" uv run python manage.py runserver 0.0.0.0:8000