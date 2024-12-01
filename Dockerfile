# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies for Flask app and additional libraries if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to tell Flask it's in production mode
ENV FLASK_ENV=production

# Run the Flask app with Gunicorn (production-ready server)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
