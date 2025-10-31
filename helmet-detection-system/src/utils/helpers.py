import cv2
import numpy as np
from datetime import datetime

def draw_bounding_box(image, box, label, color, confidence=None):
    """Draw bounding box with label on image"""
    x1, y1, x2, y2 = map(int, box)
    
    # Draw rectangle
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    
    # Create label text
    label_text = label
    if confidence:
        label_text += f" {confidence:.2f}"
    
    # Draw label background
    label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
    cv2.rectangle(image, (x1, y1 - label_size[1] - 10), 
                  (x1 + label_size[0], y1), color, -1)
    
    # Draw label text
    cv2.putText(image, label_text, (x1, y1 - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    return image

def save_violation_image(image, license_plate, violation_type="no_helmet"):
    """Save violation image with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"violation_{license_plate}_{timestamp}.jpg"
    filepath = f"data/outputs/{filename}"
    
    cv2.imwrite(filepath, image)
    return filepath

def preprocess_image(image, target_size=(640, 640)):
    """Preprocess image for model inference"""
    # Resize image
    image_resized = cv2.resize(image, target_size)
    
    # Normalize pixel values
    image_normalized = image_resized.astype(np.float32) / 255.0
    
    # Convert to channel-first format (if needed)
    image_channel_first = np.transpose(image_normalized, (2, 0, 1))
    
    return np.expand_dims(image_channel_first, axis=0)