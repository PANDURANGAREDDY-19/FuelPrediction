import numpy as np
from deepface import DeepFace
from config.settings import VERIFICATION_THRESHOLD
from .face_detector import FaceDetector

class FaceVerifier:
    def __init__(self):
        self.detector = FaceDetector()
        self.threshold = VERIFICATION_THRESHOLD
        self.model_name = "Facenet"
    
    def calculate_distance(self, embedding1, embedding2):
        """Calculate Euclidean distance between embeddings"""
        return np.linalg.norm(embedding1 - embedding2)
    
    def calculate_similarity(self, embedding1, embedding2):
        """Calculate cosine similarity between embeddings"""
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        return dot_product / (norm1 * norm2)
    
    def verify_faces(self, image_path1, image_path2):
        """Verify if two images contain the same person"""
        try:
            result = DeepFace.verify(
                img1_path=str(image_path1),
                img2_path=str(image_path2),
                model_name=self.model_name,
                detector_backend="mtcnn",
                enforce_detection=True
            )
            
            return {
                'verified': result['verified'],
                'distance': result['distance'],
                'threshold': result['threshold'],
                'similarity': 1 - (result['distance'] / result['threshold'])
            }
        except Exception as e:
            return {
                'verified': False,
                'error': str(e)
            }
    
    def verify_embeddings(self, embedding1, embedding2):
        """Verify using pre-computed embeddings"""
        distance = self.calculate_distance(embedding1, embedding2)
        similarity = self.calculate_similarity(embedding1, embedding2)
        verified = distance < self.threshold
        
        return {
            'verified': verified,
            'distance': float(distance),
            'similarity': float(similarity),
            'threshold': self.threshold
        }
    
    def match_against_database(self, candidate_image, database_embeddings):
        """Match candidate against database of embeddings"""
        candidate_data = self.detector.detect_and_extract(candidate_image)
        candidate_embedding = candidate_data['embedding']
        
        matches = []
        for db_id, db_embedding in database_embeddings.items():
            result = self.verify_embeddings(candidate_embedding, db_embedding)
            if result['verified']:
                matches.append({
                    'id': db_id,
                    'similarity': result['similarity'],
                    'distance': result['distance']
                })
        
        # Sort by similarity
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches
