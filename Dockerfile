# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for dlib, face_recognition, and Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libboost-thread-dev \
    libmagic1 \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Install npm dependencies and build CSS
RUN npm install && npm run build:css

# Install Python dependencies in stages to reduce memory usage
# Install numpy first as it's needed by other packages
RUN pip install --no-cache-dir numpy==2.3.4

# Install dlib with single-threaded build to reduce memory
ENV DLIB_NO_GUI_SUPPORT=1
RUN pip install --no-cache-dir dlib==20.0.0 --verbose

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads sorted

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Run with gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 300 --graceful-timeout 300 --keep-alive 5 wsgi:app
