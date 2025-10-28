"""
Model loading and caching utilities
"""

import streamlit as st
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from config import MODEL_NAME, DEVICE


@st.cache_resource
def load_caption_model():
    """
    Load and cache the BLIP image captioning model
    
    Returns:
        tuple: (processor, model, device)
    """
    try:
        # Determine device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load processor and model
        processor = BlipProcessor.from_pretrained(MODEL_NAME)
        model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
        
        # Move model to device
        model = model.to(device)
        model.eval()  # Set to evaluation mode
        
        return processor, model, device
    
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, "cpu"


def check_model_loaded(processor, model):
    """
    Check if model is properly loaded
    
    Args:
        processor: BLIP processor
        model: BLIP model
        
    Returns:
        bool: True if loaded successfully
    """
    return processor is not None and model is not None