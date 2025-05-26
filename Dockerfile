# Dockerfile

# 1. Use an official Python runtime as a parent image (use a specific slim version)
FROM python:3.12-slim-bookworm 

# 2. Set environment variables
# Prevents python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents python from buffering stdout/stderr 
ENV PYTHONUNBUFFERED=1
# 3. Create and set the working directory
WORKDIR /app 

# 4. Install system dependencies if needed (e.g., for psycopg)
# RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client && rm -rf /var/lib/apt/lists/*
# (Note: Using psycopg[binary] often avoids needing system deps)

# 5. Install Python dependencies
# Upgrade pip first
RUN pip install --upgrade pip 
# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy project code into the container
COPY . .

# 7. Expose the port the app runs on
EXPOSE 8000

# 8. Define the command to run the application using Gunicorn
# Replace 'myproject.wsgi:application' with your actual project's WSGI entry point
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]