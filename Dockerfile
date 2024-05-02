# Use Python 3.8 as a base image
FROM python:3.8-slim

# Install necessary dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt file
COPY requirements.txt /app/requirements.txt

# Install opencv-python and opencv-contrib-python from requirements.txt
RUN pip install -r /app/requirements.txt

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Specify the entry point of the container
ENTRYPOINT ["python", "src/main.py"]