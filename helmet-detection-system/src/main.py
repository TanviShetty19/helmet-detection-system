#!/usr/bin/env python3
"""
Main entry point for the Helmet Detection System
"""

import argparse
import cv2
from processing.video_processor import VideoProcessor
from utils.config import Config

def main():
    parser = argparse.ArgumentParser(description='Helmet Detection System')
    parser.add_argument('--input', type=str, required=True, 
                       help='Input video file path or camera index')
    parser.add_argument('--output', type=str, default='output_video.mp4',
                       help='Output video file path')
    parser.add_argument('--camera', action='store_true',
                       help='Use camera input instead of video file')
    
    args = parser.parse_args()
    
    # Initialize configuration
    config = Config()
    
    # Initialize video processor
    processor = VideoProcessor(config)
    
    try:
        if args.camera:
            # Use camera (default camera index 0)
            processor.process_camera(camera_index=0, output_path=args.output)
        else:
            # Process video file
            processor.process_video(args.input, args.output)
            
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
    except Exception as e:
        print(f"Error during processing: {str(e)}")

if __name__ == "__main__":
    main()