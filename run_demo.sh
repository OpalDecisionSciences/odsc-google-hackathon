#!/bin/bash

# AI Agent Orchestration System - Google Hackathon Demo Launcher
# Professional containerized deployment

echo "🚀 AI Agent Orchestration System - Google Hackathon Demo"
echo "=========================================================="
echo "🐳 Professional containerized Gradio interface"
echo "🎥 All agents visible simultaneously for screen recording"
echo "🔒 Local deployment only (share=False)"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Set environment variables
export COMPOSE_PROJECT_NAME=ai-agent-hackathon
export GEMINI_API_KEY=${GEMINI_API_KEY:-demo_mode}

# Create necessary directories
mkdir -p memory_data logs

echo "🔧 Building and starting containerized demo..."
echo "📡 Will be available at: http://localhost:7860"
echo ""

# Build and run with docker-compose
docker-compose up --build

echo ""
echo "🎬 Demo interface started successfully!"
echo "🎯 Perfect for Google Hackathon screen recording"
echo "📋 Activity log includes timestamps for submission"
echo ""
echo "To stop: docker-compose down"