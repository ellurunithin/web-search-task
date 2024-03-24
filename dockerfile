# Use a specific version instead of latest to ensure reproducibility.
FROM alpine:3.16

# Combine the update, the package installations, and the removal of the cache into a single RUN command
# to reduce the number of layers in the image and to ensure that the cache is not stored in the layer.
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev && \
    pip install --upgrade pip && \
    rm -rf /var/cache/apk/*

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements.txt file first to leverage Docker cache layers
COPY requirements.txt /app/

# Install Python dependencies in a single layer
RUN pip --no-cache-dir install -r requirements.txt

# Copy the rest of the application
COPY . /app

# Command to run the application
CMD ["python3", "server.py"]