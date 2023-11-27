# Use an official Python runtime as a parent image
FROM python:3.8-slim


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 80

# Command to run your application
CMD ["python3", "benchmark.py"]



# ADD app.py .
# RUN pip install requests flask matplotlib
# EXPOSE 80
# CMD ["python", "-m" , "flask", "run", "--port=80"]
