"""
Reorganize Dataset - Convert flat structure to person-based folders
"""

import shutil
from pathlib import Path
from collections import defaultdict

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def reorganize_split(split_name):
    """Reorganize one split (train/valid/test)"""
    source_dir = Path(f"data/raw/aug/{split_name}/images")
    target_dir = Path(f"data/processed/{split_name}")
    
    if not source_dir.exists():
        print(f"⚠ {split_name} not found")
        return 0
    
    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Group images by person ID
    person_images = defaultdict(list)
    for img_file in source_dir.glob("*.jpg"):
        person_id = img_file.stem.split('_')[0]
        person_images[person_id].append(img_file)
    
    # Copy to person folders
    for person_id, images in person_images.items():
        person_folder = target_dir / person_id
        person_folder.mkdir(exist_ok=True)
        
        for img_file in images:
            shutil.copy2(img_file, person_folder / img_file.name)
    
    print(f"✓ {split_name.upper()}: {len(person_images)} persons, {sum(len(imgs) for imgs in person_images.values())} images")
    return len(person_images)

def main():
    print_header("📁 REORGANIZING DATASET")
    
    print("Converting flat structure to person-based folders...")
    print("Source: data/raw/aug/[split]/images/")
    print("Target: data/processed/[split]/[person_id]/\n")
    
    total_persons = 0
    for split in ['train', 'valid', 'test']:
        count = reorganize_split(split)
        total_persons += count
    
    print_header("✅ REORGANIZATION COMPLETE")
    print(f"\nTotal unique persons: {total_persons}")
    print("\n📁 New structure:")
    print("data/processed/")
    print("├── train/")
    print("│   ├── 0000/  (5 images)")
    print("│   ├── 0001/  (5 images)")
    print("│   └── ...")
    print("├── valid/")
    print("└── test/")
    
    print("\n🎯 Next step:")
    print("python train_model.py")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
