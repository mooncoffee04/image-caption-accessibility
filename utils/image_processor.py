"""
Image preprocessing utilities for the accessibility app
"""

from PIL import Image
import numpy as np
import io


def load_image(uploaded_file):
    """
    Load and validate an uploaded image file
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        PIL Image object or None if invalid
    """
    try:
        image = Image.open(uploaded_file)
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def resize_image(image, max_size=800):
    """
    Resize image while maintaining aspect ratio
    
    Args:
        image: PIL Image object
        max_size: Maximum dimension (width or height)
        
    Returns:
        Resized PIL Image
    """
    width, height = image.size
    
    # Calculate new dimensions
    if width > height:
        if width > max_size:
            new_width = max_size
            new_height = int((max_size / width) * height)
        else:
            return image
    else:
        if height > max_size:
            new_height = max_size
            new_width = int((max_size / height) * width)
        else:
            return image
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def prepare_image_for_model(image):
    """
    Prepare image for model input (basic preprocessing)
    
    Args:
        image: PIL Image object
        
    Returns:
        Preprocessed PIL Image
    """
    # Ensure RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize if too large (to avoid memory issues)
    image = resize_image(image, max_size=800)
    
    return image


def get_image_info(image):
    """
    Get basic information about the image
    
    Args:
        image: PIL Image object
        
    Returns:
        Dictionary with image information
    """
    width, height = image.size
    
    return {
        "width": width,
        "height": height,
        "format": image.format,
        "mode": image.mode,
        "size_kb": None  # Can be calculated from bytes if needed
    }