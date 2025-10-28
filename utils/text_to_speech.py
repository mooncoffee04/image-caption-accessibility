"""
Text-to-Speech utilities
"""

from gtts import gTTS
import os
from config import TTS_LANGUAGE, TTS_SLOW, AUDIO_FORMAT


def text_to_speech(text, filename="output.mp3", lang=TTS_LANGUAGE, slow=TTS_SLOW, speed=1.0):
    """
    Convert text to speech and save as audio file
    
    Args:
        text: Text to convert to speech
        filename: Output filename
        lang: Language code (default 'en')
        slow: Whether to speak slowly
        
    Returns:
        str: Path to generated audio file, or None if error
    """
    try:
        # Create TTS object
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Save to file
        tts.save(filename)
        
        return filename
    
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None


def generate_audio_for_caption(caption, output_dir="audio_outputs"):
    """
    Generate audio file for a caption
    
    Args:
        caption: Caption text to convert
        output_dir: Directory to save audio files
        
    Returns:
        str: Path to audio file or None
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate unique filename based on timestamp
        import time
        timestamp = int(time.time() * 1000)
        filename = os.path.join(output_dir, f"caption_{timestamp}.{AUDIO_FORMAT}")
        
        # Generate speech
        return text_to_speech(caption, filename=filename)
    
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None


def cleanup_audio_files(output_dir="audio_outputs", max_files=10):
    """
    Clean up old audio files to save space
    
    Args:
        output_dir: Directory containing audio files
        max_files: Maximum number of files to keep
    """
    try:
        if not os.path.exists(output_dir):
            return
        
        # Get all audio files
        files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) 
                if f.endswith(f'.{AUDIO_FORMAT}')]
        
        # Sort by modification time
        files.sort(key=os.path.getmtime)
        
        # Delete oldest files if exceeding max
        while len(files) > max_files:
            oldest_file = files.pop(0)
            try:
                os.remove(oldest_file)
            except:
                pass
    
    except Exception as e:
        print(f"Error cleaning up audio files: {e}")