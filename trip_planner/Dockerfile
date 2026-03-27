FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
EXPOSE 8081

# Update start.sh to be more robust
RUN echo '#!/bin/sh\n\
python mcp_server.py & \n\
# Give MCP server a second to start\n\
sleep 2\n\
# Start ADK web UI on the port Cloud Run expects\n\
exec adk web adk_agent.py --port 8080 --host 0.0.0.0' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
