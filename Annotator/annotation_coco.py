import os
import json
import shutil
from PIL import Image
from tqdm import tqdm
from pathlib import Path

DATASET_DIR = Path(r"C:\Projects\MastersThesis\HMISorter\dest")
OUTPUT_DIR = Path(r"C:\Projects\MastersThesis\Annotator\results\coco")

def convert_to_coco(dataset_dir, output_dir):
    class_names = sorted([x for x in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, x))])
    class_to_id = {name: idx for idx, name in enumerate(class_names)}

    images_dir = output_dir / "images"
    os.makedirs(images_dir, exist_ok=True)

    annotation = {
        "info": {"description": "Converted dataset"},
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

    for class_name in tqdm(class_names, desc="Processing classes"):
        src_folder = dataset_dir / class_name

        images = [img for img in os.listdir(src_folder) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]

        for img_name in images:
            src_path = src_folder / img_name
            dst_name = f"{class_name}_{img_name}"
            dst_path = images_dir / dst_name

            shutil.copy2(src_path, dst_path)

            try:
                with Image.open(dst_path) as img:
                    width, height = img.size
            except Exception as e:
                print(f"Skipping {dst_name} due to error: {e}")
                continue

            annotation["images"].append({
                "id": image_id,
                "file_name": dst_name,
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

    output_json_path = output_dir / "dataset.json"
    with open(output_json_path, 'w') as f:
        json.dump(annotation, f, indent=2)

    print(f"Saved annotations to: {output_json_path}")

# Example call
convert_to_coco(
    dataset_dir=DATASET_DIR,
    output_dir=OUTPUT_DIR
)