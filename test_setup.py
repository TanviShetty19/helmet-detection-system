#!/usr/bin/env python3
"""
Test script to verify the basic setup
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from utils.config import Config
    from detection.vehicle_detector import VehicleDetector
    from processing.video_processor import VideoProcessor
    
    print("✅ All modules imported successfully!")
    
    # Test configuration
    config = Config()
    print("✅ Configuration loaded successfully!")
    
    # Test vehicle detector
    detector = VehicleDetector(config)
    print("✅ Vehicle detector initialized successfully!")
    
    print("\n🎉 Basic setup verification completed!")
    print("\nNext steps:")
    print("1. Add sample videos to data/samples/")
    print("2. Run: python src/main.py --input data/samples/sample.mp4 --output data/outputs/output.mp4")
    
except Exception as e:
    print(f"❌ Error during setup test: {e}")