"""
AI Image Narrator - Accessible Image Description Tool
Main Streamlit Application
"""

import streamlit as st
from PIL import Image
import os

# Import custom modules
from models.model_loader import load_caption_model, check_model_loaded
from utils.image_processor import load_image, prepare_image_for_model, get_image_info
from utils.caption_generator import generate_caption, format_caption_for_speech
from utils.text_to_speech import generate_audio_for_caption, cleanup_audio_files
from utils.ocr_processor import load_ocr_reader, extract_text_from_image, format_ocr_results, has_text
from config import (
    APP_TITLE, APP_SUBTITLE, APP_DESCRIPTION, 
    INSTRUCTIONS, MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS
)
import streamlit.components.v1 as components
from utils.ui_audio_feedback import UI_DESCRIPTIONS

from utils.voice_commands import (
    check_speech_recognition_available, 
    load_recognizer, 
    listen_for_command, 
    parse_command,
    get_voice_command_help
)


# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def inject_accessibility_script():
    """Inject JavaScript for audio feedback on UI interactions"""
    accessibility_js = """
    <script>
    // Announce focused elements
    document.addEventListener('focusin', function(e) {
        const element = e.target;
        let announcement = '';
        
        if (element.tagName === 'BUTTON') {
            announcement = element.textContent + ' button';
        } else if (element.tagName === 'INPUT') {
            if (element.type === 'file') {
                announcement = 'File upload. Press Enter to browse files.';
            } else if (element.type === 'checkbox') {
                const checked = element.checked ? 'checked' : 'unchecked';
                announcement = element.labels[0]?.textContent + ' checkbox, ' + checked;
            }
        } else if (element.tagName === 'SELECT') {
            announcement = element.labels[0]?.textContent + ' dropdown. Use arrow keys to navigate.';
        }
        
        if (announcement && 'speechSynthesis' in window) {
            speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(announcement);
            utterance.rate = 1.0;
            speechSynthesis.speak(utterance);
        }
    });
    
    // Announce page loads
    window.addEventListener('load', function() {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance('Page loaded. Use Tab to navigate.');
            speechSynthesis.speak(utterance);
        }
    });
    </script>
    """
    components.html(accessibility_js, height=0)

def main():
    """Main application function"""
    
    # Title and description
    st.title(APP_TITLE)
    # Inject accessibility features
    inject_accessibility_script()
    st.markdown(f"### {APP_SUBTITLE}")
    st.markdown(APP_DESCRIPTION)
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("📖 Instructions")
        st.markdown("""
        ### ⌨️ Keyboard Shortcuts:
        - **Tab**: Navigate between elements
        - **Enter/Space**: Activate buttons
        - **Arrow Keys**: Navigate dropdowns
        - **Escape**: Close dialogs
        """)
        st.markdown(INSTRUCTIONS)
        
        st.divider()
        
        # Settings
        st.header("⚙️ Settings")
        detail_level = st.selectbox(
            "Caption Detail Level",
            options=["brief", "detailed", "very_detailed"],
            index=1,
            help="Choose how detailed you want the image description"
        )
        
        enable_ocr = st.checkbox(
            "Extract Text (OCR)",
            value=True,
            help="Extract any text visible in the image"
        )
        
        auto_play = st.checkbox(
            "Auto-play Audio",
            value=True,  # Default ON for accessibility
            help="Automatically play audio description"
        )
        
        audio_speed = st.select_slider(
            "Audio Speed",
            options=["0.75x (Slow)", "1.0x (Normal)", "1.25x (Fast)", "1.5x (Faster)"],
            value="1.0x (Normal)",
            help="Adjust playback speed for comfortable listening"
        )

        st.divider()

        # Voice commands section
        if check_speech_recognition_available():
            st.header("🎤 Voice Commands")
            enable_voice = st.checkbox(
                "Enable Voice Commands",
                value=False,
                help="Use voice to control the app hands-free"
            )
            
            if enable_voice:
                st.info("Click button below and speak a command")
                if st.button("🎙️ Start Voice Command", use_container_width=True):
                    with st.spinner("🎧 Listening..."):
                        recognizer = load_recognizer()
                        command = listen_for_command(recognizer)
                        if command:
                            action = parse_command(command)
                            st.success(f"Heard: '{command}'")
                            if action:
                                st.session_state['voice_action'] = action
                            else:
                                st.warning("Command not recognized. Say 'help' for available commands.")
                        else:
                            st.warning("No command detected. Please try again.")
                
                with st.expander("📋 Available Commands"):
                    st.markdown(get_voice_command_help())
        else:
            st.warning("⚠️ Voice commands unavailable. Install: pip install SpeechRecognition pyaudio")
    
    # Load models with spinner
    with st.spinner("🔄 Loading AI models... This may take a moment on first run."):
        processor, model, device = load_caption_model()
        
        if enable_ocr:
            ocr_reader = load_ocr_reader()
        else:
            ocr_reader = None
    
    # Check if models loaded successfully
    if not check_model_loaded(processor, model):
        st.error("❌ Failed to load captioning model. Please refresh the page.")
        return
    
    st.success("✅ Models loaded successfully!")

    # Announce to user
    if auto_play:
        components.html("""
        <script>
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance('Models loaded successfully. You can now upload an image.');
            utterance.rate = 1.0;
            window.speechSynthesis.speak(utterance);
        }
        </script>
        """, height=0)
    
    # File uploader with camera option
    st.divider()
    st.header("📸 Capture or Upload Image")
    
    # Add camera option
    input_method = st.radio(
        "How would you like to provide an image?",
        options=["📷 Take Photo with Camera", "📁 Upload from Device"],
        index=0,  # Default to camera for accessibility
        help="Camera is recommended for blind users - just point and click!"
    )
    
    uploaded_file = None
    
    if input_method == "📷 Take Photo with Camera":
        st.info("📸 Press the button below to open your camera and take a photo")
        camera_image = st.camera_input("Take a picture")
        if camera_image:
            uploaded_file = camera_image
            # Audio announcement
            if auto_play:
                components.html("""
                <script>
                if ('speechSynthesis' in window) {
                    const utterance = new SpeechSynthesisUtterance('Photo captured. Processing now.');
                    utterance.rate = 1.0;
                    window.speechSynthesis.speak(utterance);
                }
                </script>
                """, height=0)
    else:
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=ALLOWED_EXTENSIONS,
            help=f"Maximum file size: {MAX_FILE_SIZE_MB}MB"
        )
    
    # Process uploaded image
    if uploaded_file is not None:
        # Load image
        image = load_image(uploaded_file)
        
        if image is None:
            st.error("❌ Failed to load image. Please try another file.")
            return
        else:
            # Announce image uploaded
            if auto_play:
                components.html("""
                <script>
                if ('speechSynthesis' in window) {
                    const utterance = new SpeechSynthesisUtterance('Image uploaded successfully. Analyzing now.');
                    utterance.rate = 1.0;
                    window.speechSynthesis.speak(utterance);
                }
                </script>
                """, height=0)
        
        # Display image
        st.divider()
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📷 Your Image")
            st.image(image, use_column_width=True)
            
            # Image info
            img_info = get_image_info(image)
            st.caption(f"Size: {img_info['width']} × {img_info['height']} pixels")
        
        with col2:
            st.subheader("🤖 AI Analysis")
            
            # Initialize session state for voice commands and auto-analyze
            if 'voice_action' not in st.session_state:
                st.session_state['voice_action'] = None
            if 'last_uploaded_file' not in st.session_state:
                st.session_state['last_uploaded_file'] = None
            
            # Check if this is a new upload
            is_new_upload = (st.session_state['last_uploaded_file'] != uploaded_file.name)
            if is_new_upload:
                st.session_state['last_uploaded_file'] = uploaded_file.name
                st.info("🔄 Auto-analyzing image...")

            analyze_button = st.button(
                "🔍 Re-analyze Image", 
                type="secondary", 
                use_container_width=True,
                help="Click to analyze again with different settings"
            )

            # Auto-analyze on new upload OR manual button click OR voice command
            should_analyze = is_new_upload or analyze_button or st.session_state.get('voice_action') == 'analyze'
            
            if should_analyze:
                # Clear voice action after use
                if st.session_state.get('voice_action') == 'analyze':
                    st.session_state['voice_action'] = None
                
                # Prepare image
                processed_image = prepare_image_for_model(image)
                
                # Generate caption
                with st.spinner("🧠 Analyzing image..."):
                    caption = generate_caption(
                        processed_image, 
                        processor, 
                        model, 
                        device, 
                        detail_level
                    )
                
                # Display caption
                st.markdown("#### 📝 Description:")
                st.info(caption)

                # Announce completion
                if auto_play:
                    components.html(f"""
                    <script>
                    if ('speechSynthesis' in window) {{
                        const utterance = new SpeechSynthesisUtterance('Analysis complete. Description is ready.');
                        utterance.rate = 1.0;
                        window.speechSynthesis.speak(utterance);
                    }}
                    </script>
                    """, height=0)

                # OCR Processing
                ocr_text = ""
                if enable_ocr and ocr_reader:
                    with st.spinner("📄 Extracting text..."):
                        ocr_data = extract_text_from_image(processed_image, ocr_reader)
                        
                        if has_text(ocr_data):
                            ocr_formatted = format_ocr_results(ocr_data)
                            st.markdown("#### 📄 Text Found in Image:")
                            st.success(ocr_formatted)
                            ocr_text = f" {ocr_formatted}"
                        else:
                            st.markdown("#### 📄 Text Found in Image:")
                            st.warning("No text detected in this image.")

                # Combine caption and OCR for audio
                full_description = format_caption_for_speech(caption) + ocr_text

                # Generate audio
                with st.spinner("🔊 Generating audio..."):
                    audio_file = generate_audio_for_caption(full_description)

                if audio_file and os.path.exists(audio_file):
                    st.markdown("#### 🔊 Listen to Description:")
                    
                    # Audio player
                    with open(audio_file, 'rb') as audio:
                        audio_bytes = audio.read()
                        st.audio(audio_bytes, format='audio/mp3')
                        
                        # Add speed control info
                        speed_text = audio_speed.split()[0]  # Extract "1.0x" from "1.0x (Normal)"
                        st.caption(f"🎚️ Playing at {speed_text}")
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Audio",
                        data=audio_bytes,
                        file_name="image_description.mp3",
                        mime="audio/mp3"
                    )
                    
                    # Cleanup old audio files
                    cleanup_audio_files()
                else:
                    st.warning("⚠️ Could not generate audio. But you can still read the description above!")
        
        # Additional info section
        st.divider()
        with st.expander("ℹ️ About This Tool"):
            st.markdown("""
            This tool uses state-of-the-art AI models to help visually impaired users understand images:
            
            - **Image Captioning**: BLIP (Bootstrapping Language-Image Pre-training) model from Salesforce
            - **Text Extraction**: EasyOCR for detecting text in images
            - **Text-to-Speech**: Google Text-to-Speech (gTTS) for audio narration
            
            **Privacy**: All processing happens in real-time. Images are not stored or saved.
            
            **Feedback**: This tool is designed to be accessible. If you have suggestions for improvement, 
            please let us know!
            """)
    
    else:
        # Show sample instruction when no image uploaded
        st.info("👆 Please upload an image to get started!")
        
        st.markdown("""
        ### What This Tool Can Do:
        
        ✅ **Describe Images**: Get detailed AI-generated descriptions of any image  
        ✅ **Read Text**: Extract and read any text visible in the image  
        ✅ **Audio Narration**: Listen to descriptions with text-to-speech  
        ✅ **Adjustable Detail**: Choose brief, detailed, or very detailed descriptions  
        ✅ **Accessible Design**: High contrast, keyboard navigation, screen reader friendly  
        
        ### Perfect For:
        - Understanding photos sent by friends and family
        - Reading signs, labels, and documents
        - Exploring visual content on the web
        - Learning about your surroundings
        """)


if __name__ == "__main__":
    main()