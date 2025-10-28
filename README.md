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