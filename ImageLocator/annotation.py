import os
import json
import random
import shutil
from PIL import Image
from tqdm import tqdm
from pathlib import Path

def split_and_convert_to_coco(dataset_dir, output_dir, train_ratio=0.8, seed=42):
    random.seed(seed)

    ignored = {"other"}
    class_names = sorted([x for x in os.listdir(dataset_dir) if x not in ignored])
    class_to_id = {name: idx for idx, name in enumerate(class_names)}

    os.makedirs(f"{output_dir}/images/train", exist_ok=True)
    os.makedirs(f"{output_dir}/images/val", exist_ok=True)

    train_images, val_images = [], []

    for class_name in tqdm(class_names, desc="Splitting dataset"):
        src_folder = os.path.join(dataset_dir, class_name)
        if not os.path.isdir(src_folder):
            continue

        images = [
            img for img in os.listdir(src_folder)
            if img.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        random.shuffle(images)
        split_index = int(len(images) * train_ratio)
        train_list = images[:split_index]
        val_list = images[split_index:]

        for phase, img_list in zip(['train', 'val'], [train_list, val_list]):
            for img_name in img_list:
                src_path = os.path.join(src_folder, img_name)
                dst_path = os.path.join(output_dir, 'images', phase, f"{class_name}_{img_name}")
                shutil.copy2(src_path, dst_path)

                phase_list = train_images if phase == 'train' else val_images
                phase_list.append((dst_path, class_name))

    for phase, data in zip(['train', 'val'], [train_images, val_images]):
        annotation = {
            "info": {"description": f"{phase} set"},
            "licenses": [],
            "images": [],
            "annotations": [],
            "categories": [
                {"id": idx, "name": name, "supercategory": "none"}
                for name, idx in class_to_id.items()
            ]
        }

        annotation_id = 1
        image_id = 1
        for img_path, class_name in tqdm(data, desc=f"Creating {phase}.json"):
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
            except:
                continue

            relative_path = os.path.relpath(img_path, os.path.join(output_dir, 'images', phase))

            annotation["images"].append({
                "id": image_id,
                "file_name": relative_path,
                "width": width,
                "height": height
            })

            annotation["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": class_to_id[class_name],
                "bbox": [0, 0, width, height],
                "area": width * height,
                "iscrowd": 0
            })

            image_id += 1
            annotation_id += 1

        with open(f"{output_dir}/annotations_{phase}.json", 'w') as f:
            json.dump(annotation, f, indent=2)

        print(f"Saved {phase} annotations to: annotations_{phase}.json")

# Example call
split_and_convert_to_coco(
    dataset_dir=r"C:\Projects\MastersThesis\ImageLocator\dest",
    output_dir=r"C:\Projects\MastersThesis\ImageLocator\annotations",
    train_ratio=0.8
)