#!/bin/bash

# Build the Docker container using the Dockerfile in the current directory
echo "Building docker container"
docker build -t benchmarking:latest .

# Run the Python script inside the Docker container
echo "Running benchmark.py inside the docker container"
docker run benchmarking