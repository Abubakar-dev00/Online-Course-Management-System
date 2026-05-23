# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies for Tkinter and MySQL client
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    tcl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Set PYTHONPATH so the app module can be found
ENV PYTHONPATH=/app

# Run the setup script to initialize DB and then run the main application
CMD ["sh", "-c", "python db_setup.py && python app/main.py"]
