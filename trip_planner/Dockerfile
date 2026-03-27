FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Ensure MCP URL is local in container
ENV MCP_URL=http://127.0.0.1:8081/get-trip

EXPOSE 8080
EXPOSE 8081

# Update start.sh to navigate to the adk_agent directory
RUN echo '#!/bin/sh\n\
echo "Step 1: Starting MCP Data Server on 8081..."\n\
python mcp_server.py > mcp.log 2>&1 & \n\
sleep 5\n\
echo "Step 2: Starting ADK Web Interface on 8080..."\n\
# Navigate to the adk_agent directory before starting\n\
cd adk_agent\n\
exec adk web mcp_trip_app/agent.py --port 8080 --host 0.0.0.0' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
