"""
Face Recognition Model Training - Keras 3.x Compatible
"""

import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

print_header("🚀 FACE RECOGNITION MODEL TRAINING")

# Import Keras
import keras
from keras import layers, models, optimizers, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.applications import MobileNetV2
import pickle
import numpy as np

print(f"Using Keras {keras.__version__}")

# Check dataset
train_path = Path("data/processed/train")
if not train_path.exists():
    print("\n❌ Dataset not found!")
    print("Run: python reorganize_dataset.py")
    sys.exit(1)

num_classes = len([d for d in train_path.iterdir() if d.is_dir()])
print(f"Found {num_classes} unique persons\n")

# Data generators
print_header("Creating Data Generators")

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    validation_split=0.2
)

train_gen = train_datagen.flow_from_directory(
    'data/processed/train',
    target_size=(160, 160),
    batch_size=32,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_gen = train_datagen.flow_from_directory(
    'data/processed/train',
    target_size=(160, 160),
    batch_size=32,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

print(f"✓ Training: {train_gen.samples} images, {train_gen.num_classes} classes")
print(f"✓ Validation: {val_gen.samples} images")

# Build model
print_header("Building Model")

base_model = MobileNetV2(
    input_shape=(160, 160, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer=optimizers.Adam(0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(f"✓ Model built: {model.count_params():,} parameters")

# Train
print_header("Training Model")

cb = [
    callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True,
        verbose=1
    ),
    callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2,
        verbose=1
    )
]

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=10,
    callbacks=cb,
    verbose=1
)

# Evaluate
print_header("Evaluation")

loss, acc = model.evaluate(val_gen, verbose=0)
print(f"Validation Loss: {loss:.4f}")
print(f"Validation Accuracy: {acc:.4f} ({acc:.2%})")

# Save
print_header("Saving Model")

models_dir = Path("src/image_processing/models")
models_dir.mkdir(parents=True, exist_ok=True)

model_path = models_dir / "face_recognition_model.h5"
history_path = models_dir / "training_history.pkl"
classes_path = models_dir / "class_indices.pkl"

model.save(model_path)

with open(history_path, 'wb') as f:
    pickle.dump(history.history, f)

with open(classes_path, 'wb') as f:
    pickle.dump(train_gen.class_indices, f)

print(f"✓ Model: {model_path}")
print(f"✓ History: {history_path}")
print(f"✓ Classes: {classes_path}")

print_header("✅ TRAINING COMPLETE")
print(f"\n📊 Final Results:")
print(f"  Validation Accuracy: {acc:.2%}")
print(f"  Model Size: {model_path.stat().st_size / 1024 / 1024:.1f} MB")
print(f"  Classes: {num_classes} persons")
print(f"\n🎯 Next: python test_model.py")
