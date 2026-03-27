FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run expects the app to listen on the specified port
EXPOSE 8080
EXPOSE 8081

# Create a start script to run both processes
# adk web --port 8080 launches the interactive UI
RUN echo '#!/bin/sh\n\
python mcp_server.py & \n\
adk web --port 8080 --host 0.0.0.0 adk_agent.py' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
