import cv2
import time
from detection.vehicle_detector import VehicleDetector
from utils.config import Config

class VideoProcessor:
    def __init__(self, config):
        self.config = config
        self.vehicle_detector = VehicleDetector(config)
        self.frame_count = 0
    
    def process_video(self, input_path, output_path):
        """Process video file for helmet detection"""
        try:
            cap = cv2.VideoCapture(input_path)
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            print(f"Processing video: {input_path}")
            print(f"Video properties: {width}x{height} at {fps} FPS")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every nth frame (for efficiency)
                if self.frame_count % self.config.FRAME_SKIP == 0:
                    processed_frame = self.process_frame(frame)
                    out.write(processed_frame)
                else:
                    out.write(frame)
                
                self.frame_count += 1
                
                # Display progress
                if self.frame_count % 100 == 0:
                    print(f"Processed {self.frame_count} frames...")
            
            cap.release()
            out.release()
            print(f"Processing complete. Output saved to: {output_path}")
            
        except Exception as e:
            print(f"Error processing video: {e}")
    
    def process_camera(self, camera_index=0, output_path=None):
        """Process camera feed in real-time"""
        cap = cv2.VideoCapture(camera_index)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            processed_frame = self.process_frame(frame)
            
            # Display the frame
            cv2.imshow('Helmet Detection System', processed_frame)
            
            # Save frame if output path provided
            if output_path and self.frame_count % 30 == 0:  # Save every 30 frames
                cv2.imwrite(f"{output_path}_frame_{self.frame_count}.jpg", processed_frame)
            
            self.frame_count += 1
            
            # Break on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def process_frame(self, frame):
        """Process a single frame for vehicle and helmet detection"""
        try:
            # Detect vehicles
            vehicles = self.vehicle_detector.detect_vehicles(frame)
            
            # Draw bounding boxes for detected vehicles
            for vehicle in vehicles:
                bbox = vehicle['bbox']
                class_name = vehicle['class_name']
                confidence = vehicle['confidence']
                
                # Choose color based on vehicle type
                if class_name in ['motorcycle', 'bicycle']:
                    color = self.config.BOX_COLORS['without_helmet']  # Red for two-wheelers
                else:
                    color = (255, 255, 255)  # White for other vehicles
                
                # Draw bounding box
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
                
                # Add label
                label = f"{class_name} {confidence:.2f}"
                cv2.putText(frame, label, (bbox[0], bbox[1] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            return frame
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            return frame