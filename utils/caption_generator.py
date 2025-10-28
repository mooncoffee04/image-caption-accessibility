"""
Caption generation utilities
"""

import torch
from config import CAPTION_LENGTHS


def generate_caption(image, processor, model, device, detail_level="detailed"):
    """
    Generate image caption with specified detail level
    
    Args:
        image: PIL Image object
        processor: BLIP processor
        model: BLIP model
        device: torch device (cuda/cpu)
        detail_level: "brief", "detailed", or "very_detailed"
        
    Returns:
        str: Generated caption
    """
    try:
        # Get length parameters
        length_params = CAPTION_LENGTHS.get(detail_level, CAPTION_LENGTHS["detailed"])
        
        # Process image
        inputs = processor(image, return_tensors="pt").to(device)
        
        # Generate caption
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_length=length_params["max_length"],
                min_length=length_params["min_length"],
                num_beams=5,
                temperature=1.0
            )
        
        # Decode caption
        caption = processor.decode(output[0], skip_special_tokens=True)
        
        # Capitalize first letter and add period if missing
        caption = caption.strip()
        if caption:
            caption = caption[0].upper() + caption[1:]
            if not caption.endswith('.'):
                caption += '.'
        
        return caption
    
    except Exception as e:
        return f"Error generating caption: {e}"


def generate_multiple_captions(image, processor, model, device, num_captions=3):
    """
    Generate multiple diverse captions for the same image
    
    Args:
        image: PIL Image object
        processor: BLIP processor
        model: BLIP model
        device: torch device
        num_captions: Number of captions to generate
        
    Returns:
        list: List of generated captions
    """
    try:
        captions = []
        inputs = processor(image, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=50,
                num_beams=5,
                num_return_sequences=num_captions,
                temperature=1.0,
                do_sample=True
            )
        
        for output in outputs:
            caption = processor.decode(output, skip_special_tokens=True)
            caption = caption.strip()
            if caption:
                caption = caption[0].upper() + caption[1:]
                if not caption.endswith('.'):
                    caption += '.'
                captions.append(caption)
        
        return captions
    
    except Exception as e:
        return [f"Error generating captions: {e}"]


def format_caption_for_speech(caption, include_prefix=True):
    """
    Format caption to be more natural for text-to-speech
    
    Args:
        caption: Raw caption string
        include_prefix: Whether to include "This image shows" prefix
        
    Returns:
        str: Formatted caption for speech
    """
    if include_prefix:
        return f"This image shows: {caption}"
    return caption