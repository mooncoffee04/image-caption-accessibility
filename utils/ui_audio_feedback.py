"""
UI Audio Feedback - Read UI elements aloud for navigation
"""

from gtts import gTTS
import os
import base64


def generate_ui_audio(text, filename="ui_feedback.mp3"):
    """
    Generate audio for UI feedback
    
    Args:
        text: Text to speak
        filename: Output filename
        
    Returns:
        str: Path to audio file
    """
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error generating UI audio: {e}")
        return None


def get_audio_base64(file_path):
    """
    Convert audio file to base64 for embedding
    
    Args:
        file_path: Path to audio file
        
    Returns:
        str: Base64 encoded audio
    """
    try:
        with open(file_path, 'rb') as f:
            audio_bytes = f.read()
        return base64.b64encode(audio_bytes).decode()
    except Exception as e:
        print(f"Error encoding audio: {e}")
        return None


def create_audio_button_html(button_text, button_label, key="btn"):
    """
    Create HTML button with hover audio feedback
    
    Args:
        button_text: Text shown on button
        button_label: What to announce when hovered
        key: Unique key for button
        
    Returns:
        str: HTML string with audio feedback
    """
    # Generate audio
    audio_file = f"ui_audio_{key}.mp3"
    generate_ui_audio(button_label, audio_file)
    
    if not os.path.exists(audio_file):
        return f'<button>{button_text}</button>'
    
    # Get base64 audio
    audio_b64 = get_audio_base64(audio_file)
    
    html = f"""
    <audio id="audio_{key}" preload="auto">
        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
    </audio>
    <button 
        onmouseover="document.getElementById('audio_{key}').play()" 
        onfocus="document.getElementById('audio_{key}').play()"
        style="
            padding: 12px 24px;
            font-size: 16px;
            background-color: #1E88E5;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
        "
    >
        {button_text}
    </button>
    """
    
    # Cleanup audio file
    try:
        os.remove(audio_file)
    except:
        pass
    
    return html


# UI Element descriptions for accessibility
UI_DESCRIPTIONS = {
    "upload": "Upload image button. Press Enter to open file picker.",
    "analyze": "Analyze image button. Press Enter to start AI analysis.",
    "reanalyze": "Re-analyze image button. Press Enter to analyze again with new settings.",
    "detail_level": "Caption detail level selector. Use arrow keys to change detail level.",
    "enable_ocr": "Extract text checkbox. Press Space to toggle text extraction.",
    "auto_play": "Auto-play audio checkbox. Press Space to toggle automatic audio playback.",
    "voice_command": "Start voice command button. Press Enter to begin listening for voice commands.",
    "download_audio": "Download audio button. Press Enter to download audio description.",
}


def get_element_description(element_key):
    """
    Get audio description for UI element
    
    Args:
        element_key: Key identifying the UI element
        
    Returns:
        str: Description text
    """
    return UI_DESCRIPTIONS.get(element_key, "Interactive element. Press Enter to activate.")