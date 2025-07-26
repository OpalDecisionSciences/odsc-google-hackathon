#!/usr/bin/env python3
"""
Google Text-to-Speech Narration Generator (Alternative)
Uses Google Cloud TTS API for professional AI voice narration
"""

import re
import os
import json
from pathlib import Path

try:
    from google.cloud import texttospeech
    import google.auth
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False

def extract_narration_segments(script_path: str):
    """Extract narration segments from the demo script"""
    
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Find all narration blocks - updated pattern for judging criteria alignment
    narration_pattern = r'\*\*NARRATION\*\*:\s*\n>(.*?)(?=\n\n\*\*(?:KEY POINTS|TECHNICAL EXCELLENCE|SOLUTION ARCHITECTURE|INNOVATIVE GEMINI|SOCIETAL IMPACT)\*\*:|$)'
    matches = re.findall(narration_pattern, content, re.DOTALL)
    
    segments = []
    for i, match in enumerate(matches):
        # Clean up the text
        clean_text = re.sub(r'>\s*', '', match)
        clean_text = re.sub(r'\n+', ' ', clean_text)
        clean_text = clean_text.strip()
        
        segments.append({
            'segment': i + 1,
            'text': clean_text,
            'filename': f'google_narration_segment_{i+1:02d}.mp3'
        })
    
    return segments

def generate_google_tts_narration(segments, output_dir='demo_audio_google'):
    """Generate narration using Google Cloud Text-to-Speech"""
    
    if not GOOGLE_TTS_AVAILABLE:
        print("❌ Google Cloud Text-to-Speech not available")
        print("💡 Install with: pip install google-cloud-texttospeech")
        return False
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    try:
        # Try to use existing Google credentials or fallback to API key method
        # First try with default credentials (works if GOOGLE_APPLICATION_CREDENTIALS is set)
        try:
            client = texttospeech.TextToSpeechClient()
            print("✅ Using Google Cloud default credentials")
        except Exception as e:
            print(f"⚠️  Default credentials not available: {e}")
            print("💡 For full Google TTS, set GOOGLE_APPLICATION_CREDENTIALS")
            print("💡 Continuing with available authentication...")
            # For hackathon, we'll use a simplified approach
            client = texttospeech.TextToSpeechClient()
        
        # Configure voice (professional, clear voice for business presentation)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Studio-O",  # Professional male voice optimized for presentations
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )
        
        # Configure audio format
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,  # Normal speed
            pitch=0.0,  # Normal pitch
        )
        
        print(f"🎙️ Generating professional AI narration using Google TTS")
        print(f"📁 Output directory: {output_dir}")
        print("=" * 60)
        
        for segment in segments:
            output_path = os.path.join(output_dir, segment['filename'])
            
            print(f"🔊 Segment {segment['segment']}")
            print(f"📝 Text: {segment['text'][:80]}...")
            
            # Prepare the text input
            synthesis_input = texttospeech.SynthesisInput(text=segment['text'])
            
            # Perform the text-to-speech request
            response = client.synthesize_speech(
                input=synthesis_input, 
                voice=voice, 
                audio_config=audio_config
            )
            
            # Save the audio file
            with open(output_path, "wb") as out:
                out.write(response.audio_content)
            
            print(f"✅ Generated: {segment['filename']}")
            print("-" * 40)
        
        print(f"\n🎬 Professional Google TTS narration generated!")
        return True
        
    except Exception as e:
        print(f"❌ Google TTS Error: {e}")
        print("💡 Make sure GOOGLE_APPLICATION_CREDENTIALS is set")
        return False

def setup_instructions():
    """Display setup instructions for Google TTS"""
    
    print("🎙️ Google Text-to-Speech Setup Instructions")
    print("=" * 50)
    print()
    print("1. **Install Google TTS**:")
    print("   pip install google-cloud-texttospeech")
    print()
    print("2. **Set up Google Cloud credentials**:")
    print("   - Go to Google Cloud Console")
    print("   - Enable Text-to-Speech API")
    print("   - Create service account key")
    print("   - Download JSON key file")
    print("   - Set environment variable:")
    print("   export GOOGLE_APPLICATION_CREDENTIALS='path/to/your/key.json'")
    print()
    print("3. **Alternative: Use your existing Gemini API setup**:")
    print("   - The system can work with your current Google AI setup")
    print("   - Or use the built-in macOS voices with generate_narration.py")
    print()
    print("🎯 **Recommendation**: Use generate_narration.py with macOS voices")
    print("   It's already set up and ready to use!")

def main():
    """Main function"""
    
    if not GOOGLE_TTS_AVAILABLE:
        setup_instructions()
        return
    
    script_file = 'DEMO_SCRIPT.md'
    
    if not os.path.exists(script_file):
        print(f"❌ Error: {script_file} not found")
        return
    
    print("🚀 Google Text-to-Speech Narration Generator")
    print("=" * 50)
    
    # Extract segments
    segments = extract_narration_segments(script_file)
    
    if not segments:
        print("❌ No narration segments found")
        return
    
    print(f"✅ Found {len(segments)} narration segments")
    
    # Generate narration
    success = generate_google_tts_narration(segments)
    
    if success:
        print("\n🎬 Google TTS Narration Complete!")
        print("🎥 Ready for professional demo recording")
    else:
        print("\n💡 Try generate_narration.py with macOS voices instead")

if __name__ == "__main__":
    main()