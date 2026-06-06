#!/bin/bash

# Exit on error
set -e

echo "Starting Flask application..."

# Ensure instance directory exists
mkdir -p /app/instance

# Run migrations if needed (uncomment if using Flask-Migrate)
# flask db upgrade

# Create database if it doesn't exist (if needed)
# python -c "from pythonblog import db, create_app; app = create_app('config.py'); app.app_context().push(); db.create_all()"

# Start the application
exec "$@"
