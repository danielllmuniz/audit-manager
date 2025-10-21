#!/bin/bash
set -e

echo "Waiting for MySQL to be ready..."

# Wait for MySQL to be ready
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if python -c "
import pymysql
import os
try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'user'),
        password=os.getenv('DB_PASSWORD', 'password'),
        database=os.getenv('DB_NAME', 'audit_db')
    )
    conn.close()
    exit(0)
except Exception as e:
    exit(1)
" 2>/dev/null; then
        echo "MySQL is ready!"
        break
    fi

    attempt=$((attempt + 1))
    echo "Attempt $attempt/$max_attempts: MySQL not ready yet, waiting..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "ERROR: MySQL did not become ready in time"
    exit 1
fi

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "Migrations completed successfully!"
else
    echo "ERROR: Migrations failed"
    exit 1
fi

# Start the application
echo "Starting application..."
exec python run.py
