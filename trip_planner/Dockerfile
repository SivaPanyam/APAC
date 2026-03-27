# Use official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose both ports (8080 for Agent, 8081 for MCP)
EXPOSE 8080
EXPOSE 8081

# Create a shell script to start both processes
RUN echo '#!/bin/sh\n\
python mcp_server.py & \n\
python main.py' > start.sh && chmod +x start.sh

# Entry point starts the combined servers
CMD ["./start.sh"]
