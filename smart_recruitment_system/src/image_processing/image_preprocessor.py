import cv2
import numpy as np
from PIL import Image
from mtcnn import MTCNN
from config.settings import IMAGE_SIZE, FACE_CONFIDENCE_THRESHOLD

class ImagePreprocessor:
    def __init__(self):
        self.detector = MTCNN()
        self.target_size = IMAGE_SIZE
    
    def load_image(self, image_path):
        """Load image from file path"""
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    def detect_face(self, image):
        """Detect face in image using MTCNN"""
        results = self.detector.detect_faces(image)
        if not results:
            return None, None
        
        # Get highest confidence detection
        best_result = max(results, key=lambda x: x['confidence'])
        if best_result['confidence'] < FACE_CONFIDENCE_THRESHOLD:
            return None, None
        
        return best_result['box'], best_result['confidence']
    
    def extract_face(self, image, box):
        """Extract and align face from image"""
        x, y, width, height = box
        x, y = max(0, x), max(0, y)
        face = image[y:y+height, x:x+width]
        
        # Resize to target size
        face = cv2.resize(face, self.target_size)
        return face
    
    def preprocess(self, image_path):
        """Complete preprocessing pipeline"""
        image = self.load_image(image_path)
        box, confidence = self.detect_face(image)
        
        if box is None:
            raise ValueError("No face detected in image")
        
        face = self.extract_face(image, box)
        face_normalized = face.astype('float32') / 255.0
        
        return face_normalized, confidence
    
    def preprocess_batch(self, image_paths):
        """Preprocess multiple images"""
        results = []
        for path in image_paths:
            try:
                face, conf = self.preprocess(path)
                results.append({'path': path, 'face': face, 'confidence': conf})
            except Exception as e:
                results.append({'path': path, 'error': str(e)})
        return results
