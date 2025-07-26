#!/usr/bin/env python3
"""
AI Voice Narration Generator for Demo Video
Extracts narration text from DEMO_SCRIPT.md and generates audio files
"""

import re
import os
import subprocess
from pathlib import Path

def extract_narration_segments(script_path: str):
    """Extract narration segments from the demo script"""
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Find all narration blocks - updated pattern for judging criteria alignment
    narration_pattern = r'\*\*NARRATION\*\*:\s*\n>(.*?)(?=\n\n\*\*(?:KEY POINTS|TECHNICAL EXCELLENCE|SOLUTION ARCHITECTURE|INNOVATIVE GEMINI|SOCIETAL IMPACT)\*\*:|$)'
    matches = re.findall(narration_pattern, content, re.DOTALL)
    
    segments = []
    for i, match in enumerate(matches):
        # Clean up the text - remove > markers and extra whitespace
        clean_text = re.sub(r'>\s*', '', match)
        clean_text = re.sub(r'\n+', ' ', clean_text)
        clean_text = clean_text.strip()
        
        # Extract timing info from the script
        timing_pattern = rf'\[(\d+:\d+)\s*-\s*(\d+:\d+)\].*?{re.escape(match[:50])}'
        timing_match = re.search(timing_pattern, content, re.DOTALL)
        
        start_time = "Unknown"
        end_time = "Unknown"
        if timing_match:
            start_time = timing_match.group(1)
            end_time = timing_match.group(2)
        
        segments.append({
            'segment': i + 1,
            'start_time': start_time,
            'end_time': end_time,
            'text': clean_text,
            'filename': f'narration_segment_{i+1:02d}.aiff'
        })
    
    return segments

def generate_audio_segments(segments, voice='Alex', output_dir='demo_audio'):
    """Generate audio files for each narration segment"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"🎙️ Generating AI voice narration using voice: {voice}")
    print(f"📁 Output directory: {output_dir}")
    print("=" * 60)
    
    for segment in segments:
        output_path = os.path.join(output_dir, segment['filename'])
        
        print(f"🔊 Segment {segment['segment']}: {segment['start_time']} - {segment['end_time']}")
        print(f"📝 Text: {segment['text'][:80]}...")
        print(f"💾 Output: {segment['filename']}")
        
        # Generate audio using macOS say command
        try:
            # Create temporary text file to avoid command line issues
            temp_text_file = os.path.join(output_dir, f'temp_text_{segment["segment"]}.txt')
            with open(temp_text_file, 'w') as f:
                f.write(segment['text'])
            
            subprocess.run([
                'say', 
                '-v', voice,
                '-f', temp_text_file,  # Read from file instead of command line
                '-o', output_path
            ], check=True, capture_output=True)
            
            # Clean up temp file
            os.remove(temp_text_file)
            
            print(f"✅ Generated successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error generating audio: {e}")
        
        print("-" * 40)
    
    print(f"\n🎬 All narration segments generated in '{output_dir}/' directory")
    print("🎥 You can now use these audio files during video recording")

def list_available_voices():
    """List all available voices for narration"""
    
    print("🎙️ Available AI Voices:")
    print("=" * 40)
    
    try:
        result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True, check=True)
        voices = result.stdout.strip().split('\n')
        
        # Filter to English voices and recommend the best ones
        english_voices = []
        recommended = ['Alex', 'Samantha', 'Tom', 'Karen', 'Daniel', 'Moira']
        
        for voice_line in voices:
            if 'en_US' in voice_line:
                voice_name = voice_line.split()[0]
                english_voices.append(voice_name)
                
                marker = "⭐ RECOMMENDED" if voice_name in recommended else ""
                print(f"  {voice_name:<15} {marker}")
        
        print(f"\n💡 Recommended voices for professional demo: {', '.join(recommended[:4])}")
        return english_voices
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error listing voices: {e}")
        return []

def create_master_script(segments, output_dir='demo_audio'):
    """Create a master script file for timing reference"""
    
    script_path = os.path.join(output_dir, 'MASTER_NARRATION_SCRIPT.md')
    
    with open(script_path, 'w') as f:
        f.write("# 🎬 Master Narration Script for Demo Recording\n\n")
        f.write("**Instructions**: Play each audio file at the specified timing during screen recording\n\n")
        f.write("---\n\n")
        
        for segment in segments:
            f.write(f"## Segment {segment['segment']}: {segment['start_time']} - {segment['end_time']}\n\n")
            f.write(f"**Audio File**: `{segment['filename']}`\n\n")
            f.write(f"**Script**:\n> {segment['text']}\n\n")
            f.write("---\n\n")
        
        f.write("## 🎥 Recording Instructions\n\n")
        f.write("1. Start screen recording\n")
        f.write("2. Play each audio file at the specified timing\n") 
        f.write("3. Follow the visual actions described in DEMO_SCRIPT.md\n")
        f.write("4. Pause between segments if needed for synchronization\n")
        f.write("5. Edit final video to sync audio with screen actions\n\n")
        f.write("**🏆 Result**: Professional AI-narrated demo video for Google Hackathon!**\n")
    
    print(f"📋 Master script created: {script_path}")

def main():
    """Main function to generate AI narration"""
    
    script_file = 'DEMO_SCRIPT.md'
    
    if not os.path.exists(script_file):
        print(f"❌ Error: {script_file} not found")
        print("💡 Make sure you're running this from the project root directory")
        return
    
    print("🚀 AI Voice Narration Generator for Google Hackathon Demo")
    print("=" * 60)
    
    # List available voices
    voices = list_available_voices()
    print()
    
    # Get user choice for voice
    print("🎙️ Select voice for narration:")
    recommended_voices = ['Alex', 'Samantha', 'Tom', 'Karen']
    
    for i, voice in enumerate(recommended_voices, 1):
        print(f"  {i}. {voice}")
    
    print("  5. Custom voice name")
    
    try:
        # Auto-select Samantha for professional demo (can be changed)
        selected_voice = 'Samantha'  # Professional female voice
        print(f"🎯 Auto-selected professional voice: {selected_voice}")
        
        print(f"\n🎯 Selected voice: {selected_voice}")
        
        # Extract narration segments
        print("\n📝 Extracting narration segments from DEMO_SCRIPT.md...")
        segments = extract_narration_segments(script_file)
        
        if not segments:
            print("❌ No narration segments found in script")
            print("💡 Make sure DEMO_SCRIPT.md has **NARRATION**: blocks")
            return
        
        print(f"✅ Found {len(segments)} narration segments")
        
        # Generate audio files
        generate_audio_segments(segments, selected_voice)
        
        # Create master script
        create_master_script(segments)
        
        print("\n🎬 AI Voice Narration Setup Complete!")
        print("🎥 Ready to record professional demo video with AI narration")
        
    except KeyboardInterrupt:
        print("\n\n👋 Narration generation cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()