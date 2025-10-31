# Configuration settings for the helmet detection system

class Config:
    # Model paths
    VEHICLE_DETECTION_MODEL = "models/vehicle_detection/yolov8n.pt"
    HELMET_CLASSIFICATION_MODEL = "models/helmet_classification/helmet_model.pt"
    
    # Detection confidence thresholds
    VEHICLE_CONFIDENCE = 0.5
    HELMET_CONFIDENCE = 0.7
    LICENSE_PLATE_CONFIDENCE = 0.6
    
    # Video processing settings
    FRAME_SKIP = 5  # Process every 5th frame for efficiency
    OUTPUT_VIDEO_QUALITY = 70
    
    # License plate settings
    LICENSE_PLATE_REGION = "en"  # Change based on your country
    
    # Output settings
    SAVE_VIOLATIONS = True
    OUTPUT_DIR = "data/outputs/"
    
    # Visualization settings
    DRAW_BOUNDING_BOXES = True
    BOX_COLORS = {
        'with_helmet': (0, 255, 0),    # Green
        'without_helmet': (0, 0, 255), # Red
        'license_plate': (255, 255, 0) # Yellow
    }