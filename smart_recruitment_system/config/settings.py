import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "src" / "image_processing" / "models"

# Image Processing Settings
IMAGE_SIZE = (160, 160)
FACE_CONFIDENCE_THRESHOLD = 0.9
VERIFICATION_THRESHOLD = 0.6

# Supported Image Formats
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
