FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Create /tmp directory for file uploads
RUN mkdir -p /tmp

# Expose port
EXPOSE 80

# Run the application
CMD ["uvicorn", "src.index:app", "--host", "0.0.0.0", "--port", "80"]