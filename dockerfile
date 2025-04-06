# Use the official Python 3.10.4 image as a base image
FROM python:3.10.4

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Install netcat for waiting for PostgreSQL
RUN apt-get update && apt-get install -y netcat

# Copy the .env file into the container
COPY .env /app/.env

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to run the FastAPI app using uvicorn, ensuring it loads environment variables
CMD ["sh", "-c", "until nc -z -v -w30 postgres 5432; do echo 'Waiting for PostgreSQL...'; sleep 1; done && uvicorn main:app --host 0.0.0.0 --port 8000"]
