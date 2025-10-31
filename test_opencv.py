#!/usr/bin/env python3
import sys
import subprocess

def test_import(package_name):
    try:
        __import__(package_name)
        print(f"✅ {package_name} imported successfully")
        return True
    except ImportError as e:
        print(f"❌ {package_name} import failed: {e}")
        return False

# Test critical packages
packages = ['cv2', 'numpy', 'torch']
success = True

for package in packages:
    if not test_import(package):
        success = False

if success:
    print("\n🎉 All imports successful! Testing basic OpenCV functionality...")
    try:
        import cv2
        import numpy as np
        
        # Create a test image
        test_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Test image operations
        gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(test_img, (5, 5), 0)
        
        print("✅ Basic OpenCV operations work!")
        print(f"✅ OpenCV version: {cv2.__version__}")
        
    except Exception as e:
        print(f"❌ OpenCV functionality test failed: {e}")
else:
    print("\n❌ Some imports failed. Let's fix this...")
    
    # Install missing packages
    if not any('cv2' in p for p in packages if test_import(p)):
        print("Installing OpenCV...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python-headless"])
    
    if not test_import('numpy'):
        print("Installing numpy...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])