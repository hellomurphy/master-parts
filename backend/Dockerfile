# Use an official Python image as a base image
FROM python:3.12-alpine3.19

# Set the working directory in the container
WORKDIR /app/backend

# Copy requirements.txt to the container
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of the application code to the container
COPY /main.py /app/backend/

# Expose port 80 for the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]