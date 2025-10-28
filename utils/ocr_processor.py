"""
OCR (Optical Character Recognition) utilities
"""

import streamlit as st
import easyocr
import numpy as np
from config import OCR_LANGUAGES, OCR_CONFIDENCE_THRESHOLD


@st.cache_resource
def load_ocr_reader():
    """
    Load and cache EasyOCR reader
    
    Returns:
        easyocr.Reader object
    """
    try:
        reader = easyocr.Reader(OCR_LANGUAGES, gpu=False)
        return reader
    except Exception as e:
        st.error(f"Error loading OCR reader: {e}")
        return None


def extract_text_from_image(image, reader, confidence_threshold=OCR_CONFIDENCE_THRESHOLD):
    """
    Extract text from image using OCR
    
    Args:
        image: PIL Image object
        reader: EasyOCR reader
        confidence_threshold: Minimum confidence score to include text
        
    Returns:
        dict: Contains 'text' (string) and 'details' (list of detected items)
    """
    try:
        # Convert PIL image to numpy array
        image_np = np.array(image)
        
        # Perform OCR
        results = reader.readtext(image_np)
        
        # Filter by confidence and extract text
        extracted_text = []
        details = []
        
        for (bbox, text, confidence) in results:
            if confidence >= confidence_threshold:
                extracted_text.append(text)
                details.append({
                    'text': text,
                    'confidence': round(confidence, 2),
                    'bbox': bbox
                })
        
        # Combine all text
        full_text = ' '.join(extracted_text) if extracted_text else ""
        
        return {
            'text': full_text,
            'details': details,
            'count': len(details)
        }
    
    except Exception as e:
        return {
            'text': "",
            'details': [],
            'count': 0,
            'error': str(e)
        }


def format_ocr_results(ocr_data):
    """
    Format OCR results for display and speech
    
    Args:
        ocr_data: Dictionary from extract_text_from_image
        
    Returns:
        str: Formatted text description
    """
    if ocr_data['count'] == 0:
        return "No text detected in the image."
    
    text = ocr_data['text']
    count = ocr_data['count']
    
    if count == 1:
        return f"Found 1 text element: {text}"
    else:
        return f"Found {count} text elements: {text}"


def has_text(ocr_data):
    """
    Check if image contains any text
    
    Args:
        ocr_data: Dictionary from extract_text_from_image
        
    Returns:
        bool: True if text was found
    """
    return ocr_data['count'] > 0