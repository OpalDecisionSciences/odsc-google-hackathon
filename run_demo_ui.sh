#!/bin/bash

# AI Agent Orchestration System - Demo UI Launcher
# Perfect for Google Hackathon screen recording

echo "🚀 AI Agent Orchestration System - Live Demo UI"
echo "================================================"
echo "🎯 Perfect for Google Hackathon demonstration!"
echo "🎥 Ready for screen recording with timestamps"
echo ""
echo "📡 Starting Gradio interface on http://localhost:7860"
echo "⏰ Demo activity log includes timestamps for submission"
echo ""
echo "🧠 Available Agents:"
echo "   • Customer Support (Memory-Enhanced)"
echo "   • Sales Qualification (BANT + Learning)"
echo "   • Strategic Planning (SWOT/TOES + Intelligence)"
echo "   • Social Media Intelligence (Competitive Analysis)"
echo "   • Content Creation (Performance Learning)"
echo ""
echo "🔗 Key Demo Features:"
echo "   • Real-time agent interactions"
echo "   • Cross-agent intelligence sharing"
echo "   • Memory persistence demonstrations"
echo "   • Timestamp logging for submission"
echo ""

# Set environment variable if not set
if [ -z "$GEMINI_API_KEY" ]; then
    export GEMINI_API_KEY="demo_mode"
    echo "⚠️  GEMINI_API_KEY not set - running in demo mode"
else
    echo "✅ GEMINI_API_KEY configured"
fi

echo ""
echo "🎬 Starting demo interface..."
echo "Press Ctrl+C to stop"
echo ""

# Run the demo UI
python demo_ui.py