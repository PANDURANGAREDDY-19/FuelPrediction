import numpy as np
import cv2
from pathlib import Path
from deepface import DeepFace
from .image_preprocessor import ImagePreprocessor
from config.settings import MODELS_DIR, IMAGE_SIZE

class FaceDetectorCustom:
    """Face detector with support for custom trained models"""
    
    def __init__(self, use_custom_model=False):
        self.preprocessor = ImagePreprocessor()
        self.use_custom_model = use_custom_model
        self.custom_model = None
        
        if use_custom_model:
            self._load_custom_model()
        else:
            self.model_name = "Facenet"
    
    def _load_custom_model(self):
        """Load custom trained model"""
        from tensorflow.keras.models import load_model
        
        model_path = MODELS_DIR / "face_recognition_model.h5"
        if model_path.exists():
            self.custom_model = load_model(model_path)
            print(f"✓ Loaded custom model: {model_path}")
        else:
            print(f"⚠ Custom model not found, using pre-trained")
            self.use_custom_model = False
            self.model_name = "Facenet"
    
    def extract_embedding(self, image_path):
        """Extract face embedding"""
        if self.use_custom_model and self.custom_model:
            return self._extract_custom_embedding(image_path)
        else:
            return self._extract_pretrained_embedding(image_path)
    
    def _extract_pretrained_embedding(self, image_path):
        """Extract embedding using pre-trained model"""
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
    
    def _extract_custom_embedding(self, image_path):
        """Extract embedding using custom model"""
        img = cv2.imread(str(image_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, IMAGE_SIZE)
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)
        
        # Get embedding from second-to-last layer
        embedding_model = tf.keras.Model(
            inputs=self.custom_model.input,
            outputs=self.custom_model.layers[-2].output
        )
        embedding = embedding_model.predict(img, verbose=0)[0]
        
        return embedding
    
    def detect_and_extract(self, image_path):
        """Detect face and extract embedding"""
        face, confidence = self.preprocessor.preprocess(image_path)
        embedding = self.extract_embedding(image_path)
        
        return {
            'embedding': embedding,
            'confidence': confidence,
            'face_detected': True,
            'model': 'custom' if self.use_custom_model else 'pretrained'
        }
    
    def predict_person(self, image_path):
        """Predict person ID using custom model"""
        if not self.use_custom_model or not self.custom_model:
            raise ValueError("Custom model not loaded")
        
        img = cv2.imread(str(image_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, IMAGE_SIZE)
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)
        
        predictions = self.custom_model.predict(img, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class]
        
        return {
            'person_id': int(predicted_class),
            'confidence': float(confidence),
            'all_predictions': predictions[0].tolist()
        }
