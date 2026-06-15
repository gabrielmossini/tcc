cat > /home/mossini/Workspace/Aegis/docker/entrypoint.sh << 'EOF'
#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating default user if not exists..."
python manage.py create_default_user

echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
EOF

chmod +x /home/mossini/Workspace/Aegis/docker/entrypoint.sh