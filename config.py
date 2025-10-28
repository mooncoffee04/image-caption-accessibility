# Configuration file for Image Captioning Accessibility App

# Model Configuration
MODEL_NAME = "Salesforce/blip-image-captioning-large"
MODEL_TYPE = "blip"  # Options: "blip", "git"
DEVICE = "cpu"  # Will auto-detect GPU if available

# Caption Settings
CAPTION_LENGTHS = {
    "brief": {"max_length": 30, "min_length": 10},
    "detailed": {"max_length": 50, "min_length": 20},
    "very_detailed": {"max_length": 100, "min_length": 30}
}

# OCR Settings
OCR_LANGUAGES = ['en']  # Can add more languages: ['en', 'es', 'fr']
OCR_CONFIDENCE_THRESHOLD = 0.3

# TTS Settings
TTS_LANGUAGE = 'en'
TTS_SLOW = False
AUDIO_FORMAT = "mp3"

# UI Text Constants
APP_TITLE = "🔊 AI Image Narrator"
APP_SUBTITLE = "Accessible Image Description Tool for Visually Impaired Users"
APP_DESCRIPTION = """
This tool helps visually impaired users understand images through:
- **Detailed Image Descriptions**: AI-generated captions describing what's in the image
- **Text-to-Speech**: Automatic audio narration of descriptions
- **Text Extraction**: Read any text visible in the image (signs, labels, documents)
"""

# Accessibility Settings
HIGH_CONTRAST = True
LARGE_FONTS = True
AUTO_PLAY_AUDIO = True  # User preference for auto-playing audio

# UI Colors (High Contrast Theme)
PRIMARY_COLOR = "#1E88E5"
BACKGROUND_COLOR = "#FFFFFF"
SECONDARY_BACKGROUND = "#F0F2F6"
TEXT_COLOR = "#000000"

# File Upload Settings
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'webp', 'bmp']

# Instructions for users
INSTRUCTIONS = """
### How to Use:
1. **Upload an Image**: Click 'Browse files' or drag and drop an image
2. **Choose Detail Level**: Select how detailed you want the description
3. **Get Description**: AI will analyze and describe the image
4. **Listen**: Click play to hear the description read aloud
5. **Read Text**: Any text in the image will be extracted automatically
"""

KEYBOARD_SHORTCUTS = """
### Keyboard Navigation:
- **Tab**: Navigate between elements
- **Enter/Space**: Activate buttons
- **Arrow Keys**: Navigate options
"""

