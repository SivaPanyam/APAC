FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure MCP URL is local in container
ENV MCP_URL=http://127.0.0.1:8081/get-trip

EXPOSE 8080
EXPOSE 8081

# Update start.sh with better logging and host binding
RUN echo '#!/bin/sh\n\
echo "Starting MCP Data Server..."\n\
python mcp_server.py > mcp.log 2>&1 & \n\
sleep 5\n\
echo "Starting ADK Web Interface on port 8080..."\n\
# adk web expects either a file path or a module:attribute\n\
# --host 0.0.0.0 is crucial for Cloud Run visibility\n\
exec adk web adk_agent.py --port 8080 --host 0.0.0.0' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
