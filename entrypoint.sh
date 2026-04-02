#!/bin/bash
set -e

# Run Django migrations
python manage.py migrate --noinput

# Collect static files (continue even if it fails - e.g., S3 misconfiguration)
echo "Collecting static files..."
if python manage.py collectstatic --noinput; then
    echo "Static files collected successfully"
else
    echo "Warning: collectstatic failed. The app will still start, but static/CSS files may not load."
    echo "Check your S3/static storage configuration if CSS is missing."
fi

# Create superuser if env vars are set and user doesn't exist
if [ -n "$SUPERUSER_USERNAME" ] && [ -n "$SUPERUSER_PASSWORD" ] && [ -n "$SUPERUSER_EMAIL" ]; then
    echo "Creating superuser: $SUPERUSER_USERNAME"
    python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"
fi

# Execute the command (Gunicorn)
exec "$@"
