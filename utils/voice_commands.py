"""
Voice command utilities for hands-free operation
"""

import streamlit as st

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False


def check_speech_recognition_available():
    """Check if speech recognition is available"""
    return SPEECH_AVAILABLE


@st.cache_resource
def load_recognizer():
    """Load and cache speech recognizer"""
    if not SPEECH_AVAILABLE:
        return None
    try:
        recognizer = sr.Recognizer()
        return recognizer
    except Exception as e:
        print(f"Error loading speech recognizer: {e}")
        return None


def listen_for_command(recognizer, duration=3):
    """
    Listen for voice command
    
    Args:
        recognizer: SpeechRecognition recognizer object
        duration: How long to listen in seconds
        
    Returns:
        str: Recognized command or None
    """
    if not recognizer:
        return None
    
    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for audio
            audio = recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            
            # Recognize speech using Google Speech Recognition
            command = recognizer.recognize_google(audio).lower()
            return command
    
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        return None


def parse_command(command):
    """
    Parse voice command and return action
    
    Args:
        command: Voice command string
        
    Returns:
        str: Action to take ('analyze', 'upload', 'play', 'stop', 'help', None)
    """
    if not command:
        return None
    
    command = command.lower().strip()
    
    # Analyze commands
    if any(word in command for word in ['analyze', 'analyse', 'describe', 'caption', 'what is this', 'tell me']):
        return 'analyze'
    
    # Audio control commands
    if any(word in command for word in ['play', 'listen', 'hear', 'audio']):
        return 'play'
    
    if any(word in command for word in ['stop', 'pause', 'quiet']):
        return 'stop'
    
    # Upload commands
    if any(word in command for word in ['upload', 'new image', 'different image']):
        return 'upload'
    
    # Help command
    if any(word in command for word in ['help', 'commands', 'what can you do']):
        return 'help'
    
    return None


def get_voice_command_help():
    """
    Get help text for voice commands
    
    Returns:
        str: Help text
    """
    return """
    ### 🎤 Voice Commands:
    - **"Analyze"** or **"Describe"**: Analyze the uploaded image
    - **"Play"** or **"Listen"**: Play audio description
    - **"Stop"** or **"Pause"**: Stop audio playback
    - **"Help"**: Show available commands
    
    Say any command clearly after clicking "Start Voice Command"
    """