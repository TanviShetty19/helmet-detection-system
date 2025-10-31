import cv2
import torch
from ultralytics import YOLO
from utils.config import Config

class VehicleDetector:
    def __init__(self, config):
        self.config = config
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load YOLO model for vehicle detection"""
        try:
            # This will automatically download YOLOv8n if not present
            self.model = YOLO('yolov8n.pt')
            print("Vehicle detection model loaded successfully")
        except Exception as e:
            print(f"Error loading vehicle detection model: {e}")
    
    def detect_vehicles(self, frame):
        """Detect two-wheelers in the frame"""
        if self.model is None:
            return []
        
        try:
            # Run inference
            results = self.model(frame, verbose=False)
            
            two_wheelers = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # class 3: car, 4: motorcycle, 6: bus, 7: truck, etc.
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        # Filter for two-wheelers (motorcycles, bicycles)
                        if class_id in [1, 2, 3, 4] and confidence > self.config.VEHICLE_CONFIDENCE:  # person, bicycle, car, motorcycle
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            two_wheelers.append({
                                'bbox': [x1, y1, x2, y2],
                                'confidence': confidence,
                                'class_id': class_id,
                                'class_name': self.model.names[class_id]
                            })
            
            return two_wheelers
            
        except Exception as e:
            print(f"Error in vehicle detection: {e}")
            return []