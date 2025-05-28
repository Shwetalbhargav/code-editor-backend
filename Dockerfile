FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Node.js and required tools
RUN apt-get update && \
    apt-get install -y curl gnupg build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose your actual internal port
EXPOSE 10000

# Start FastAPI on port 10000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
