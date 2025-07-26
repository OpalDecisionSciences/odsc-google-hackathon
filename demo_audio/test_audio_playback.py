#!/usr/bin/env python3
"""
Test Audio Playback - Verify all narration files work
Run this before recording your demo
"""

import os
import subprocess
import time

def test_audio_files():
    """Test that all audio files can be played"""
    
    audio_dir = "."
    audio_files = [f"narration_segment_{i:02d}.aiff" for i in range(1, 9)]
    
    print("🎙️ Testing Audio Files for Demo Recording")
    print("=" * 50)
    
    for i, audio_file in enumerate(audio_files, 1):
        file_path = os.path.join(audio_dir, audio_file)
        
        if not os.path.exists(file_path):
            print(f"❌ Missing: {audio_file}")
            continue
            
        file_size = os.path.getsize(file_path)
        print(f"✅ Segment {i}: {audio_file} ({file_size:,} bytes)")
        
        # Test playback (macOS)
        try:
            # Play first 2 seconds of each file to test
            subprocess.run([
                'afplay', file_path, '-t', '2'
            ], check=True, timeout=3)
            print(f"   🔊 Audio test successful")
        except Exception as e:
            print(f"   ⚠️  Audio test warning: {e}")
        
        time.sleep(0.5)  # Brief pause between tests
    
    print("\n🎬 Audio Test Complete!")
    print("📋 Logic Pro Setup Instructions:")
    print("   1. Open Logic Pro X")
    print("   2. Create Empty Audio Project")
    print("   3. Import all 8 .aiff files")
    print("   4. Position according to LOGIC_PRO_SETUP_GUIDE.md")
    print("   5. Press SPACEBAR to start demo recording!")

if __name__ == "__main__":
    test_audio_files()