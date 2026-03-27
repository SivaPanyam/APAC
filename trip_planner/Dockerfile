FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV MCP_URL=http://127.0.0.1:8081/get-trip

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Cloud Run uses the PORT environment variable
EXPOSE 8080
EXPOSE 8081

# New robust startup command
# adk web expects a module:attribute or a python file.
# Running it from the directory where it can find the package
RUN echo '#!/bin/sh\n\
python mcp_server.py > mcp.log 2>&1 & \n\
sleep 3\n\
cd adk_agent\n\
exec adk web --port 8080 --host 0.0.0.0 mcp_trip_app/agent.py' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
