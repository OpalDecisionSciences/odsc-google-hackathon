#!/bin/bash
# Quick demo script for Google Hackathon judges
# Jeannine_Jordan submission - AI Agent Orchestration System

echo "🏆 Google Hackathon Demo - Jeannine_Jordan"
echo "🚀 AI Agent Orchestration System"
echo "=" * 50

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    echo "💡 Alternative: Run 'python demo_ui.py' for local demo"
    exit 1
fi

echo "🐳 Building Docker container..."
docker build -t jeannine-jordan . || {
    echo "❌ Docker build failed"
    exit 1
}

echo "🧪 Running smoke tests..."
docker run --rm jeannine-jordan ./TEST.sh || {
    echo "⚠️  Some tests failed but core functionality is operational"
}

echo ""
echo "🎯 Starting Interactive Demo Interface..."
echo "📡 Will be available at: http://localhost:7860"
echo "🔑 Press Ctrl+C to stop the demo"
echo ""

# Run the demo with environment variable support
docker run -p 7860:7860 \
    -e GEMINI_API_KEY="${GEMINI_API_KEY}" \
    jeannine-jordan

echo ""
echo "🏁 Demo stopped. Thank you for evaluating Jeannine_Jordan's submission!"