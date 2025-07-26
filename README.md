# 🚀 AI Agent Orchestration System - Jeannine_Jordan

**Google Agentic AI Hackathon Submission**: Revolutionary business intelligence platform with orchestrated AI agents and persistent memory.

## 🎯 **Agent Workflow Overview**

This system implements sophisticated agentic patterns for real-world business intelligence:

1. **Receive Input**: Business analysis requests (company research, strategy planning, customer service)
2. **Retrieve Memory**: Cross-session persistent memory with customer recognition and SWOT intelligence
3. **Plan Sub-tasks**: ReAct pattern with specialized agents (Research → Strategy → Social → Support)
4. **Call Tools**: Live APIs (Yahoo Finance, Google News) + Gemini AI for analysis
5. **Generate Response**: Coordinated intelligence sharing across all agents

### **🌟 Key Features:**
- **🔬 Live Business Intelligence**: Real-time data from Yahoo Finance, Google News, social media
- **🧠 Persistent Memory System**: Customer service remembers users by name across sessions
- **⚡ SWOT-TOWS Strategic Analysis**: Advanced strategic planning with real competitive data
- **🤖 Agent Orchestration**: 8+ specialized AI agents working in coordinated workflows
- **📊 Real Competitive Analysis**: Actual competitor data, not mock examples
- **💾 Cross-Session Persistence**: JSON-based memory that survives system restarts

## 🎪 **Live Demo Capabilities**

### **📊 Real Business Intelligence**
- Enter **"NVIDIA"** → Get live financial data, stock performance, competitor analysis
- **Dynamic Variables**: Business context flows automatically between all agents
- **Web Scraping**: Yahoo Finance, Google News, Reddit, Wikipedia integration

### **🧠 Persistent Memory System**
- **Customer Service**: Remembers users by name across sessions
- **Strategic Intelligence**: SWOT-TOWS analysis persists across system restarts
- **JSON Storage**: Docker-compatible persistent memory files
- **Cross-Session Learning**: Agents improve with each interaction

### **⚡ Advanced Agent Orchestration**
- **Research Agent**: Live data gathering and competitive intelligence
- **Strategy Agent**: SWOT-TOWS analysis with real business data
- **Customer Support**: Persistent customer recognition and history
- **Social Media Intelligence**: Real competitor monitoring and sentiment analysis

## 🎯 **Hackathon Judge Verification**

**Test 1**: Customer Memory Persistence
1. Customer says: *"Hi, my name is John Smith, I need help"*
2. Agent stores name and conversation
3. **Restart system** (simulate container restart)
4. Customer returns: *"Hi, it's John again"*
5. **✅ Agent recognizes John and references previous conversation**

**Test 2**: Real Business Intelligence
1. Enter **"NVIDIA"** in Research Agent
2. **✅ Live financial data, competitor analysis, social sentiment**
3. Use Strategy Agent → **✅ SWOT-TOWS with real competitive data**
4. **✅ Intelligence flows between all agents automatically**

## 📋 Submission Checklist

- [x] All code in `src/` runs without errors  
- [x] `ARCHITECTURE.md` contains a clear diagram sketch and explanation  
- [x] `EXPLANATION.md` covers planning, tool use, memory, and limitations  
- [x] `DEMO.md` links to a 3–5 min video with timestamped highlights  

## 🚀 **Setup Instructions**

### **Core Modules Implementation**

Our system implements the required agentic architecture:

- **`src/agents/research_agent.py`**: Planner for business intelligence sub-tasks
- **`src/core/base_agent.py`**: Executor logic with Gemini API integration  
- **`src/memory/persistent_memory.py`**: Cross-session memory storage and retrieval

### **Dependencies & Installation**

```bash
# Option 1: Docker (Recommended for Judges)
docker build -t jeannine-jordan .
docker run -p 7860:7860 jeannine-jordan

# Option 2: Local Setup
pip install -r requirements.txt
export GEMINI_API_KEY="your_api_key_here"
python demo_ui.py
```

### **Gemini API Integration**

This system **requires** Google Gemini API:

1. Get free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set environment variable: `export GEMINI_API_KEY="your_key"`
3. System demonstrates Gemini usage in all agent workflows

### **Smoke Test**

```bash
# Test core functionality
./TEST.sh

# In Docker
docker run --rm jeannine-jordan ./TEST.sh
```


## 📂 Folder Layout

![Folder Layout Diagram](images/folder-githb.png)



## 🏅 Judging Criteria

- **Technical Excellence **  
  This criterion evaluates the robustness, functionality, and overall quality of the technical implementation. Judges will assess the code's efficiency, the absence of critical bugs, and the successful execution of the project's core features.

- **Solution Architecture & Documentation **  
  This focuses on the clarity, maintainability, and thoughtful design of the project's architecture. This includes assessing the organization and readability of the codebase, as well as the comprehensiveness and conciseness of documentation (e.g., GitHub README, inline comments) that enables others to understand and potentially reproduce or extend the solution.

- **Innovative Gemini Integration **  
  This criterion specifically assesses how effectively and creatively the Google Gemini API has been incorporated into the solution. Judges will look for novel applications, efficient use of Gemini's capabilities, and the impact it has on the project's functionality or user experience. You are welcome to use additional Google products.

- **Societal Impact & Novelty **  
  This evaluates the project's potential to address a meaningful problem, contribute positively to society, or offer a genuinely innovative and unique solution. Judges will consider the originality of the idea, its potential real‑world applicability, and its ability to solve a challenge in a new or impactful way.


