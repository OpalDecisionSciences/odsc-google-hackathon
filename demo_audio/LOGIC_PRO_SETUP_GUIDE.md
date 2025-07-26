# 🎬 Logic Pro Demo Recording Setup Guide
## Complete Step-by-Step Instructions for Google Hackathon Demo

### 📋 **What You'll Create**
A professional Logic Pro project that automatically plays your narration at precise times, allowing you to focus entirely on the demo interface during recording.

---

## 🚀 **Step 1: Create New Logic Pro Project**

1. **Open Logic Pro X**
2. **Create New Project**:
   - Click "New Project"
   - Select "Empty Project"
   - Choose "Audio" (not Software Instrument)
   - Set Input: "No Input" 
   - Set Output: "Stereo Output"
   - Click "Create"

3. **Save Project**:
   - Save as: `Google_Hackathon_Demo_Audio`
   - Location: Save in your `demo_audio/` folder

---

## 🎵 **Step 2: Project Settings Configuration**

1. **Set Project Tempo** (Important!):
   - In top menu: Logic Pro → Project Settings → Synchronization
   - Set "Tempo Mode" to "Keep"
   - Set BPM to exactly **120** (this makes timing calculations easier)

2. **Set Project Length**:
   - Press **Control + ;** to open Project Settings
   - Set "Project End" to **4 minutes 30 seconds**

3. **Configure Timeline**:
   - View → Show Ruler
   - Click the ruler and select "Time" (not Bars & Beats)
   - This shows minutes:seconds instead of musical measures

---

## 🎯 **Step 3: Import Your Audio Files**

1. **Open Browser**:
   - Press **O** or View → Show Library
   - Click "All Files" tab in browser

2. **Navigate to Audio Files**:
   - Find your `demo_audio/` folder
   - You should see all 8 narration files

3. **Create Audio Track**:
   - Track → New Track → Audio
   - Name it "Demo Narration"

---

## ⏰ **Step 4: Precise Audio Placement**

### **Timeline Positions** (Copy these exactly):

1. **Segment 1 - Opening Hook**:
   - Drag `narration_segment_01.aiff` to position: **0:00.000**
   - Duration: ~15 seconds

2. **Segment 2 - Judging Criteria**:
   - Drag `narration_segment_02.aiff` to position: **0:15.000**
   - Duration: ~30 seconds

3. **Segment 3 - Technical Excellence**:
   - Drag `narration_segment_03.aiff` to position: **0:45.000**
   - Duration: ~45 seconds

4. **Segment 4 - Solution Architecture**:
   - Drag `narration_segment_04.aiff` to position: **1:30.000**
   - Duration: ~45 seconds

5. **Segment 5 - Gemini Integration**:
   - Drag `narration_segment_05.aiff` to position: **2:15.000**
   - Duration: ~45 seconds

6. **Segment 6 - Technical Architecture**:
   - Drag `narration_segment_06.aiff` to position: **3:00.000**
   - Duration: ~30 seconds

7. **Segment 7 - Societal Impact**:
   - Drag `narration_segment_07.aiff` to position: **3:30.000**
   - Duration: ~45 seconds

8. **Segment 8 - Closing**:
   - Drag `narration_segment_08.aiff` to position: **4:15.000**
   - Duration: ~15 seconds

---

## 🎨 **Step 5: Visual Organization (Color Coding)**

1. **Select Each Audio Region** and assign colors:
   - Segment 1-2 (Opening): **Blue** (Info sections)
   - Segment 3-4 (Technical): **Green** (Technical demos)
   - Segment 5-6 (Integration): **Orange** (AI demonstrations)
   - Segment 7-8 (Impact): **Purple** (Business impact)

2. **Add Region Names**:
   - Double-click each audio region
   - Rename to: "Opening", "Criteria", "Technical", "Architecture", etc.

---

## 📍 **Step 6: Add Timing Markers**

1. **Create Markers** for key demo actions:
   - Position playhead at **0:00** → Press **Option + '** → Name: "START DEMO"
   - Position playhead at **0:45** → Press **Option + '** → Name: "ENTER NVIDIA"
   - Position playhead at **1:30** → Press **Option + '** → Name: "STRATEGY AGENT"
   - Position playhead at **2:15** → Press **Option + '** → Name: "SOCIAL MEDIA"
   - Position playhead at **3:00** → Press **Option + '** → Name: "CUSTOMER SUPPORT"
   - Position playhead at **3:30** → Press **Option + '** → Name: "AMD DEMO"
   - Position playhead at **4:15** → Press **Option + '** → Name: "CLOSING"

---

## 🔊 **Step 7: Audio Optimization**

1. **Set Master Volume**:
   - Adjust main output volume to comfortable listening level
   - Test with headphones first

2. **Add Gentle Fade-ins/Fade-outs**:
   - Select each audio region
   - Drag the top-left corner to create 0.1 second fade-in
   - Drag top-right corner to create 0.1 second fade-out
   - This prevents audio "pops"

3. **Set Track Volume**:
   - Demo Narration track volume: **-6 dB** (leaves headroom)

---

## 🎬 **Step 8: Recording Preparation**

### **Pre-Recording Setup**:

1. **Save Project**: **Cmd + S**

2. **Set Playback Settings**:
   - Logic Pro → Preferences → Audio → General
   - Set "Sample Rate" to **44.1 kHz**
   - Set "Buffer Size" to **256 samples** (low latency)

3. **Disable Count-In**:
   - Record → Count-in → Off
   - This prevents the metronome click before recording

4. **Window Arrangement**:
   - Make Logic Pro window small (quarter screen)
   - Position it where you can see the playhead progress
   - Leave rest of screen for demo interface

---

## 🚀 **EXECUTION INSTRUCTIONS**

### **Recording Day Workflow**:

#### **Setup (5 minutes)**:
1. Open Logic Pro project: `Google_Hackathon_Demo_Audio`
2. Open Terminal: `cd /path/to/hackathon && python demo_ui.py`
3. Open browser to: `http://localhost:7860`
4. Start screen recording software (QuickTime/ScreenFlow/OBS)

#### **Recording Process**:

1. **Position playhead at 0:00** in Logic Pro
2. **Start screen recording**
3. **Press SPACEBAR in Logic Pro** (starts audio playback)
4. **Immediately switch to demo interface** (Cmd+Tab)
5. **Follow timing cues** from DEMO_SCRIPT.md
6. **Let Logic Pro play automatically** - don't touch it!

#### **Demo Actions Timeline**:
```
0:00-0:15: Show demo interface loading
0:15-0:45: Point to system overview, show 8 agents
0:45-1:30: Enter "NVIDIA", select "AI/Semiconductor", click "Gather Intelligence"
1:30-2:15: Select "Comprehensive" strategy, click "Generate Strategy"
2:15-3:00: Select "Competitor Analysis", click "Analyze Intelligence"
3:00-3:30: Enter customer inquiry with "Sarah Johnson"
3:30-4:15: Enter "AMD", show different analysis
4:15-4:30: Final overview, let audio finish
```

---

## 🔧 **Troubleshooting**

### **If Audio Doesn't Play**:
- Check output device: Logic Pro → Preferences → Audio → Devices
- Ensure "Built-in Output" is selected
- Check master volume fader

### **If Timing is Off**:
- Practice run without recording first
- Use the markers as visual guides
- Remember: It's okay to pause between segments if needed

### **If Logic Pro is Confusing**:
- Use **Spacebar** to play/pause
- Use **Return** to go back to beginning
- Use **Right Arrow** to skip to next marker

---

## 🏆 **Pro Tips for Perfect Recording**

1. **Practice First**: Do 2-3 dry runs to get comfortable with timing
2. **Use Two Monitors**: Logic Pro on one, demo on the other
3. **Prepare Demo Data**: Have NVIDIA/AMD ready to type quickly
4. **Stay Calm**: If you miss a timing cue, keep going - you can edit later
5. **Audio Priority**: The narration timing is most important - demo actions can be slightly off

---

## 📁 **Final Project Structure**

Your `demo_audio/` folder should contain:
```
demo_audio/
├── Google_Hackathon_Demo_Audio.logicx/     # Logic Pro project
├── narration_segment_01.aiff through 08.aiff
├── MASTER_NARRATION_SCRIPT.md
└── LOGIC_PRO_SETUP_GUIDE.md               # This file
```

---

## 🎯 **Ready to Record!**

After following this setup, you'll have:
- ✅ Professional Logic Pro project with perfect timing
- ✅ Color-coded visual organization
- ✅ Marker-based navigation
- ✅ One-button recording workflow
- ✅ Hands-free narration playback

**Press SPACEBAR and let the AI voice guide your demo!** 🚀

---

**🏆 Result**: Professional hackathon demo video with synchronized AI narration and live business intelligence demonstrations!