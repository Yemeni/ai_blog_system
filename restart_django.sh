#!/bin/bash
echo "🔄 Restarting Django..."
pkill -f "manage.py runserver"
sleep 2
python manage.py runserver 0.0.0.0:8000 &
