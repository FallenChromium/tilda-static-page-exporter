# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy only the necessary files into the container at /app
COPY requirements.txt ./

# Enable BuildKit caches for pip packages
RUN --mount=type=cache,id=pip-cache,target=/root/.cache/pip \
    pip install --trusted-host pypi.python.org -r requirements.txt

COPY app.py ./

# Expose port 5000 for the Flask application
EXPOSE 5000

# Set environment variables
ENV TILDA_PUBLIC_KEY=<your-tilda-public-key>
ENV TILDA_SECRET_KEY=<your-tilda-secret-key>
ENV LOCAL_PATH_PREFIX=<your-local-path-prefix>

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
