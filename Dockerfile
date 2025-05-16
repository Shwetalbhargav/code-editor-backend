# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy code and install dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 10000

# Startup script
CMD ["bash", "start.sh"]
