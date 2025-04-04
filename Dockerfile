# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories and initialize data
RUN mkdir -p data venv && \
    touch data/time.txt && \
    echo "Thu Mar 13 00:00:00 2025" > data/time.txt

# Set environment variables
ENV FLASK_APP=web_service.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "web_service:app"]