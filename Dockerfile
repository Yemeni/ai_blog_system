# Use official Python base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install system dependencies (Linux-specific, Windows will ignore)
RUN apt-get update && apt-get install -y gettext \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy project files
COPY . .

# Ensure script has execution permission (for Linux)
RUN chmod +x start.sh || echo "Skipping chmod on Windows"

# Expose Django's port
EXPOSE 8000

# Run the startup script instead of directly running Django
CMD ["sh", "start.sh"]
