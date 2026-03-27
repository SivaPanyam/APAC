FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV MCP_URL=http://127.0.0.1:8081/get-trip

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
EXPOSE 8081

# Enhanced startup script
RUN echo '#!/bin/sh\n\
echo "Step 1: Starting MCP Data Server on 8081..."\n\
python mcp_server.py > mcp.log 2>&1 & \n\
\n\
echo "Step 2: Starting ADK Web Interface on 8080..."\n\
# We use exec so ADK becomes PID 1 and Cloud Run can monitor it correctly\n\
exec adk web adk_agent.py --port 8080 --host 0.0.0.0' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
