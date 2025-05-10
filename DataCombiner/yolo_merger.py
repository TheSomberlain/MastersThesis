import os
import shutil
from pathlib import Path

IMAGEDIR_1_PATH = r"C:\Projects\MastersThesis\Annotator\results\yolo\images"
IMAGEDIR_2_PATH = r"C:\Projects\MastersThesis\DataCombiner\source\yolo\images"
ANNOTATIONDIR_1_PATH = r"C:\Projects\MastersThesis\Annotator\results\yolo\labels"
ANNOTATIONDIR_2_PATH = r"C:\Projects\MastersThesis\DataCombiner\source\yolo\labels"
OUTPUTIMAGEDIR_PATH = "results/yolo/images"
OUTPUTANNOTAIONDIR_PATH = "results/yolo/labels"

def combine_yolo_annotations_and_copy_images(image_dir1, image_dir2, annotation_dir1, annotation_dir2, output_image_dir, output_annotation_dir):
    # Ensure the output directories exist
    image_dir1 = Path(image_dir1)
    image_dir2 = Path(image_dir2)
    annotation_dir1 = Path(annotation_dir1)
    annotation_dir2 = Path(annotation_dir2)
    output_image_dir = Path(output_image_dir)
    output_annotation_dir = Path(output_annotation_dir)

    if output_image_dir.exists():
            shutil.rmtree(output_image_dir)
    if output_annotation_dir.exists():
            shutil.rmtree(output_annotation_dir)

    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_annotation_dir, exist_ok=True)

    # Copy images from both directories to the output
    shutil.copytree(image_dir1 / "train", output_image_dir / "train")
    for f in (image_dir2).glob("*"):
        shutil.copy(f, output_image_dir / "train")

    # Copy annotations from both directories to the output
    shutil.copytree(annotation_dir1 / "train", output_annotation_dir / "train")
    for f in (annotation_dir2).glob("*"):
        shutil.copy(f, output_annotation_dir / "train")


    shutil.copytree(image_dir1 / "val", output_image_dir / "val")
    shutil.copytree(annotation_dir1 / "val", output_annotation_dir / "val")

    print(f"Combined annotations and images copied to '{output_image_dir}' and '{output_annotation_dir}'")

# Example usage
combine_yolo_annotations_and_copy_images(
    image_dir1=IMAGEDIR_1_PATH,
    image_dir2=IMAGEDIR_2_PATH,
    annotation_dir1=ANNOTATIONDIR_1_PATH,
    annotation_dir2=ANNOTATIONDIR_2_PATH,
    output_image_dir=OUTPUTIMAGEDIR_PATH,
    output_annotation_dir=OUTPUTANNOTAIONDIR_PATH
)