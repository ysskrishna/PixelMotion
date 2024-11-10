# backend/ai_engine/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy common package first (now relative to backend directory)
COPY common/ /app/common/

# Copy ai_engine
COPY ai_engine/ /app/ai_engine/

# Set working directory to ai_engine folder
WORKDIR /app/ai_engine

# Install Python dependencies including the local package
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "worker.py"]

