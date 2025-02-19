#!/bin/sh
while true; do
    if [ -f "/app/restart.txt" ]; then
        echo "🔄 Restarting Django..."
        rm /app/restart.txt
        pkill -f "manage.py runserver"  # Kill Django process
        python manage.py runserver 0.0.0.0:8000 &  # Restart
    fi
    sleep 2
done
