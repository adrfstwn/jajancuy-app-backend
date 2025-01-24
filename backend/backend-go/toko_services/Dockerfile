# Base Image
FROM golang:1.23-slim

# Install other package
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Setting WORKDIR
WORKDIR jajancuy/toko-user_services

