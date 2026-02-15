"""
OpenCV Face Detector using Haar Cascade
"""
import cv2
import numpy as np
from pathlib import Path

class OpenCVFaceDetector:
    def __init__(self):
        # Load Haar Cascade classifier
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
    
    def detect_faces(self, image_path):
        """Detect faces using OpenCV Haar Cascade"""
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return []
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            results = []
            for (x, y, w, h) in faces:
                results.append({
                    'confidence': 0.9,
                    'box': [int(x), int(y), int(w), int(h)]
                })
            
            return results
        except Exception as e:
            return []
