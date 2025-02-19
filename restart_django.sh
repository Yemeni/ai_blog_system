#!/bin/bash

# Find the PID of the running Django process
PID=$(lsof -t -i:8000)

if [ -z "$PID" ]; then
    echo "🔴 No Django process found running on port 8000. Starting a new instance..."
else
    echo "🔴 Stopping Django process with PID $PID..."
    kill $PID
    sleep 2  # Wait a moment to ensure the process is fully terminated
fi

echo "🚀 Starting Django runserver..."
nohup python3 manage.py runserver 0.0.0.0:8000 > django.log 2>&1 &

echo "✅ Django has been restarted successfully."
