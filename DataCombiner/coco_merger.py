import os
import json
import shutil
from pathlib import Path
import random
from PIL import Image
from tqdm import tqdm
from pathlib import Path

DATASET1_JSON = Path(r"C:\Projects\MastersThesis\Annotator\results\coco\dataset.json")
DATASET2_JSON = Path(r"C:\Projects\MastersThesis\DataCombiner\source\coco\result.json")
DATASET1_IMAGES = DATASET1_JSON.parent / "images"
DATASET2_IMAGES = DATASET2_JSON.parent / "images"
OUTPUT_DIR = Path(r"C:\Projects\MastersThesis\DataCombiner\results\coco")
TRAIN_RATIO = 0.8
SEED = 42

def load_coco(json_path, images_dir, force_override_filename=False):
    """Load COCO JSON and correct dirty file names if needed."""
    with open(json_path) as f:
        coco = json.load(f)
    images = coco['images']
    annotations = coco['annotations']

    for img in images:
        if force_override_filename:
            # Always use only the clean filename, ignore what JSON says
            img_name = Path(img['file_name']).name
            possible_file = images_dir / img_name
            if possible_file.exists():
                img['file_name'] = img_name
                img['full_path'] = possible_file
            else:
                # As fallback, try to find by ID pattern (you must ensure your images are named properly like {id}.png)
                id_based_name = f"{img['id']}.png"
                possible_file = images_dir / id_based_name
                if possible_file.exists():
                    img['file_name'] = id_based_name
                    img['full_path'] = possible_file
                else:
                    raise FileNotFoundError(f"Image not found for {img['file_name']} nor {id_based_name}")
        else:
            img['full_path'] = images_dir / img['file_name']
    return images, annotations, coco['categories']

def clean_dataset2_filenames(json_path, images_dir):
    """Force re-linking dataset2 file names by using the actual images folder, ignoring dataset2 JSON paths."""
    with open(json_path) as f:
        coco = json.load(f)

    annotations = coco['annotations']
    categories = coco['categories']

    # Build actual images list in the folder
    actual_images = list(images_dir.glob("*.*"))
    actual_images_map = {img.name: img for img in actual_images}

    # Check if we have the same number of images as in JSON
    if len(coco['images']) != len(actual_images):
        print(f"WARNING: JSON has {len(coco['images'])} images, folder has {len(actual_images)} images.")
        # You can decide here to stop or continue with warnings

    # Relink images by naive order (or you can customize to your logic)
    clean_images = []
    for i, img_obj in enumerate(coco['images']):
        if i >= len(actual_images):
            raise RuntimeError("Mismatch between dataset2.json and actual images folder")
        actual_img = actual_images[i]
        clean_img = {
            "id": img_obj['id'],  # Keep original ID
            "file_name": actual_img.name,
            "width": img_obj['width'],
            "height": img_obj['height'],
            "full_path": actual_img  # Path object
        }
        clean_images.append(clean_img)

    return clean_images, annotations, categories

def merge_coco(images1, ann1, images2, ann2):
    """Merge two datasets and remap IDs."""
    merged_images = []
    merged_annotations = []
    new_image_id = 1
    new_ann_id = 1
    old_to_new_img_id = {}

    # Merge images from both datasets
    for img in images1 + images2:
        old_id = img['id']
        new_img = {
            "id": new_image_id,
            "file_name": f"{new_image_id}_{img['file_name']}",
            "width": img['width'],
            "height": img['height'],
            "full_path": img['full_path']
        }
        merged_images.append(new_img)
        old_to_new_img_id[old_id] = new_image_id
        new_image_id += 1

    # Merge annotations and update image_id
    for ann in ann1 + ann2:
        new_ann = ann.copy()
        new_ann['id'] = new_ann_id
        new_ann['image_id'] = old_to_new_img_id[ann['image_id']]
        merged_annotations.append(new_ann)
        new_ann_id += 1

    return merged_images, merged_annotations

def split_dataset(images, annotations, train_ratio, seed):
    """Split images and annotations into train and val."""
    random.seed(seed)
    random.shuffle(images)
    split_idx = int(len(images) * train_ratio)
    train_images = images[:split_idx]
    val_images = images[split_idx:]

    train_img_ids = {img['id'] for img in train_images}
    val_img_ids = {img['id'] for img in val_images}

    train_annotations = [ann for ann in annotations if ann['image_id'] in train_img_ids]
    val_annotations = [ann for ann in annotations if ann['image_id'] in val_img_ids]

    return (train_images, train_annotations), (val_images, val_annotations)

def save_coco(images, annotations, categories, output_json, output_images_dir):
    """Save COCO JSON and copy images."""
    output_images_dir.mkdir(parents=True, exist_ok=True)
    coco = {
        "info": {"description": "Merged Dataset"},
        "licenses": [],
        "categories": categories,
        "images": [],
        "annotations": annotations
    }

    for img in tqdm(images, desc=f"Copying images to {output_images_dir.name}"):
        dst_name = img['file_name']
        shutil.copy2(img['full_path'], output_images_dir / dst_name)
        coco['images'].append({
            "id": img['id'],
            "file_name": dst_name,
            "width": img['width'],
            "height": img['height']
        })

    with open(output_json, 'w') as f:
        json.dump(coco, f, indent=2)
    print(f"Saved {output_json}")

# === EXECUTION ===

# Load datasets
images1, ann1, categories1 = load_coco(DATASET1_JSON, DATASET1_IMAGES)
images2, ann2, _ = clean_dataset2_filenames(DATASET2_JSON, DATASET2_IMAGES)

# Merge
merged_images, merged_annotations = merge_coco(images1, ann1, images2, ann2)

# Split
(train_images, train_ann), (val_images, val_ann) = split_dataset(merged_images, merged_annotations, TRAIN_RATIO, SEED)

# Save train
save_coco(train_images, train_ann, categories1, OUTPUT_DIR / "train.json", OUTPUT_DIR / "images" / "train")

# Save val
save_coco(val_images, val_ann, categories1, OUTPUT_DIR / "val.json", OUTPUT_DIR / "images" / "val")