# image-caption-accessibility
AI-powered image captioning tool for visually impaired users. 

### Core Features:

Detailed Image Descriptions - Not just "a dog on grass" but "a golden retriever playing with a red ball on green grass in a park"
Text-to-Speech Integration - Automatically read captions aloud so users don't need to read screen text
Scene Understanding - Describe the overall context (indoor/outdoor, time of day, activities happening)
Object Detection + Counting - "There are 3 people in this image, 2 chairs, and 1 table"
Text Extraction (OCR) - Read any text visible in images (signs, labels, documents)
Color Information - Describe dominant colors since that's often useful context

### User-Friendly Design for Accessibility:

- Large buttons and high contrast UI
- Keyboard navigation support
- Voice commands to trigger photo capture (if using webcam)
- Multiple input methods: upload, webcam, or paste URL

### Tech Stack:

- Image Captioning: Pre-trained models like BLIP, BLIP-2, or GIT (faster and good quality)
- Object Detection: YOLO or DETR for detailed object info
- OCR: EasyOCR or Tesseract for text extraction
- Text-to-Speech: gTTS (Google Text-to-Speech) or pyttsx3
- Streamlit for the interface
---

# 🔊 AI Image Narrator

An accessible image description tool designed specifically for visually impaired users. This application uses state-of-the-art AI models to generate detailed image descriptions, extract text from images, and provide audio narration.

## ✨ Features

- **🤖 AI Image Captioning**: Generates natural language descriptions of images using BLIP model
- **📝 Multiple Detail Levels**: Choose between brief, detailed, or very detailed descriptions
- **📄 Text Extraction (OCR)**: Automatically detects and reads text visible in images
- **🔊 Text-to-Speech**: Converts descriptions to audio for easy listening
- **♿ Accessibility First**: High contrast design, keyboard navigation, screen reader friendly
- **⚡ Fast & Free**: Runs locally or deploys easily to Streamlit Cloud
- **🔒 Privacy Focused**: No data storage - all processing happens in real-time

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd image-caption-accessibility
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open in browser**
The app will automatically open at `http://localhost:8501`

## 📦 Project Structure

```
image-caption-accessibility/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── config.py                   # Configuration settings
├── models/
│   └── model_loader.py        # Model loading utilities
├── utils/
│   ├── image_processor.py     # Image preprocessing
│   ├── caption_generator.py   # Caption generation
│   ├── text_to_speech.py      # TTS functionality
│   └── ocr_processor.py       # OCR text extraction
├── .streamlit/
│   └── config.toml            # Streamlit theme config
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🎯 How to Use

1. **Upload an Image**: Click "Browse files" or drag and drop an image
2. **Choose Settings**: Select detail level and enable/disable OCR in the sidebar
3. **Analyze**: Click the "Analyze Image" button
4. **Listen**: Audio description plays automatically (if enabled) or click play
5. **Download**: Save the audio description for offline use

### Supported Image Formats
- PNG
- JPG/JPEG
- WEBP
- BMP

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Image Captioning**: BLIP (Salesforce)
- **OCR**: EasyOCR
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Deep Learning**: PyTorch, Transformers (Hugging Face)
- **Image Processing**: Pillow, OpenCV

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy!

### Other Options
- **Hugging Face Spaces**: Deploy as a Gradio/Streamlit Space
- **Railway.app**: One-click deployment
- **Render.com**: Free tier available
- **Local Network**: Run on local network for personal use

## ⚙️ Configuration

Edit `config.py` to customize:

- **Model selection**: Change the BLIP model variant
- **Caption lengths**: Adjust detail levels
- **OCR settings**: Add more languages
- **UI text**: Customize instructions and descriptions
- **Accessibility options**: Modify colors and themes

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add support for video description
- [ ] Multi-language support for captions
- [ ] Object detection with bounding boxes
- [ ] Batch processing for multiple images
- [ ] Camera/webcam integration
- [ ] Save history of analyzed images
- [ ] Voice commands for hands-free operation

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Salesforce Research**: BLIP model
- **Hugging Face**: Transformers library
- **EasyOCR Team**: OCR capabilities
- **Streamlit**: Amazing framework for ML apps

## 📧 Contact

For questions, suggestions, or feedback, please open an issue on GitHub.

## 🌟 Show Your Support

If this tool helps you or someone you know, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs or issues
- 💡 Suggesting new features
- 🔄 Sharing with others who might benefit

---

**Made with ❤️ for accessibility and inclusion**