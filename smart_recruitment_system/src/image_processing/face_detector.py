import numpy as np
from deepface import DeepFace
from .image_preprocessor import ImagePreprocessor

class FaceDetector:
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.model_name = "Facenet"
    
    def extract_embedding(self, image_path):
        """Extract face embedding using DeepFace"""
        try:
            embedding = DeepFace.represent(
                img_path=str(image_path),
                model_name=self.model_name,
                enforce_detection=True,
                detector_backend="mtcnn"
            )
            return np.array(embedding[0]['embedding'])
        except Exception as e:
            raise ValueError(f"Failed to extract embedding: {str(e)}")
    
    def detect_and_extract(self, image_path):
        """Detect face and extract embedding"""
        face, confidence = self.preprocessor.preprocess(image_path)
        embedding = self.extract_embedding(image_path)
        
        return {
            'embedding': embedding,
            'confidence': confidence,
            'face_detected': True
        }
    
    def detect_multiple_faces(self, image_path):
        """Detect multiple faces in an image"""
        try:
            faces = DeepFace.extract_faces(
                img_path=str(image_path),
                detector_backend="mtcnn",
                enforce_detection=False
            )
            return len(faces), faces
        except:
            return 0, []
