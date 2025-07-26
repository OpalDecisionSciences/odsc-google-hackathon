# AI Agent Orchestration System - Google Hackathon
# Professional Gradio Demo Interface

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make TEST.sh executable for hackathon smoke tests
RUN chmod +x TEST.sh

# Create necessary directories
RUN mkdir -p memory_data logs

# Expose Gradio port
EXPOSE 7860

# Environment variables
ENV PYTHONPATH="/app/src"
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Run the demo UI
CMD ["python", "demo_ui.py"]