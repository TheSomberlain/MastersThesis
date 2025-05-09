import os
import shutil
import random
from pathlib import Path
from PIL import Image

def split_and_prepare_yolo_data(source_dir, dest_dir, class_names, split_ratio=0.8):
    """
    Splits image data into train/val, creates YOLO labels, and copies files.

    :param source_dir: Root folder with class-named subfolders of images
    :param dest_dir: Root folder to store `images/train`, `images/val`, `labels/train`, `labels/val`
    :param class_names: List of class names
    :param split_ratio: Fraction of images used for training
    """

    # Prepare destination subfolders
    for subset in ['train', 'val']:
        for subfolder in ['images', 'labels']:
            folder = Path(dest_dir) / subfolder / subset
            folder.mkdir(parents=True, exist_ok=True)
            # Clear contents
            for f in folder.glob("*"):
                f.unlink()

    class_map = {name: idx for idx, name in enumerate(class_names)}

    for class_name in os.listdir(source_dir):
        class_path = Path(source_dir) / class_name
        if not class_path.is_dir() or class_name not in class_map:
            continue

        class_id = class_map[class_name]
        image_files = [f for f in class_path.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]
        random.shuffle(image_files)

        split_idx = int(len(image_files) * split_ratio)
        train_files = image_files[:split_idx]
        val_files = image_files[split_idx:]

        for subset, files in zip(['train', 'val'], [train_files, val_files]):
            for img_path in files:
                # Copy image
                dst_img_path = Path(dest_dir) / 'images' / subset / img_path.name
                shutil.copy2(img_path, dst_img_path)

                # Get image size
                with Image.open(img_path) as img:
                    w, h = img.size

                # Create dummy label file (full image box)
                label_path = Path(dest_dir) / 'labels' / subset / (img_path.stem + '.txt')
                with open(label_path, 'w') as f:
                    f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")

    print("✅ Dataset split and YOLO-format data prepared.")

# === CONFIG ===
source_dir = "dest"         # Contains subfolders named after classes
dest_dir = "yolov5"                       # Will contain images/train, images/val, labels/train, labels/val
class_names = ['bargraph', 'chart', 'damper', 'fan', 'line', 'mixer',
               'motor', 'nav', 'pump', 'status', 'tag', 'value', 'valve', 'pipe']

split_and_prepare_yolo_data(source_dir, dest_dir, class_names, split_ratio=0.8)