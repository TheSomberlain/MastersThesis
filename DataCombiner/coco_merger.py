import os
import json
import shutil
from pathlib import Path

DATASET1_PATH = r"c:\Projects\MastersThesis\Annotator\results\coco\annotations"
DATASET2_PATH = r"C:\Projects\MastersThesis\DataCombiner\source\coco"
OUTPUT_PATH = "results/coco"

def merge_coco_datasets(
    dataset1_path,
    dataset2_path,
    output_path
):
    dataset1_path = Path(dataset1_path)
    dataset2_path = Path(dataset2_path)
    output_path = Path(output_path)
    output_images = output_path / "images"
    output_json = output_path / "train.json"

    if output_path.exists():
            shutil.rmtree(output_path)

    output_images.mkdir(parents=True, exist_ok=True)

    with open(dataset1_path / "train.json") as f:
        coco1 = json.load(f)
    with open(dataset2_path / "result.json") as f:
        coco2 = json.load(f)

    # Prepare new dataset
    merged = {
        "info": coco1.get("info", {}),
        "licenses": coco1.get("licenses", []),
        "categories": coco1["categories"],
        "images": [],
        "annotations": []
    }

    # Track ID offsets
    image_id_offset = max(img["id"] for img in coco1["images"]) + 1
    annotation_id_offset = max(ann["id"] for ann in coco1["annotations"]) + 1

    # Copy dataset1 as-is
    image_id_map = {}
    for img in coco1["images"]:
        merged["images"].append(img)
        src_image = dataset1_path / "images/train" / img["file_name"]
        dst_image = output_images / img["file_name"]
        shutil.copy2(src_image, dst_image)

    merged["annotations"].extend(coco1["annotations"])

    # Merge dataset2 with updated IDs
    for img in coco2["images"]:
        old_id = img["id"]
        new_id = image_id_offset
        image_id_offset += 1

        image_id_map[old_id] = new_id

        new_img = img.copy()
        new_img["id"] = new_id
        merged["images"].append(new_img)

        # Copy image
        src_image = dataset2_path / "images" / os.path.basename(img["file_name"])
        dst_image = output_images / os.path.basename(img["file_name"])
        if not dst_image.exists():
            shutil.copy2(src_image, dst_image)


    for ann in coco2["annotations"]:
        old_image_id = ann["image_id"]
        if old_image_id not in image_id_map:
            print(f"Warning: image_id {old_image_id} not found in image_id_map, skipping annotation {ann['id']}")
            continue  # Skip annotations with unknown image_id
        new_ann = ann.copy()
        new_ann["id"] = annotation_id_offset
        annotation_id_offset += 1
        new_ann["image_id"] = image_id_map[ann["image_id"]]
        merged["annotations"].append(new_ann)

    # Write merged annotation
    with open(output_json, "w") as f:
        json.dump(merged, f, indent=2)

    dataset1_val_path = dataset1_path / "val.json"
    shutil.copy2(dataset1_val_path, output_path / "val.json")
    print(f"Merged dataset saved to: {output_path}")

# Example usage
merge_coco_datasets(DATASET1_PATH, DATASET2_PATH, OUTPUT_PATH)