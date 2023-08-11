# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy global_params.yml to the container
COPY global_params.yml /app

# Install any needed packages specified in requirements.txt
RUN pip install influxdb-client

# Run the script when the container launches
CMD ["python", "insert_into_influxdb.py"]
