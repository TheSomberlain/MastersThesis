import torch
from PIL import Image
import pandas as pd
import cv2
import numpy as np
import sys
import os
import pathlib
sys.modules["pathlib._local"] = pathlib 
if os.name == 'nt':
   pathlib.PosixPath = pathlib.WindowsPath
else:
   pathlib.WindowsPath = pathlib.PosixPath
from pathlib import Path

path = Path('../ModelTrainer/yolov5/runs/train/exp2/weights/best.pt').resolve()
model = torch.hub.load('../ModelTrainer/yolov5/', 'custom', path=str(path), source='local', force_reload=True)

def process_with_yolo(image_path):
    results = model(image_path)
    results.render()
    
    rendered_image = results.ims[0]

    rendered_image_rgb = cv2.cvtColor(rendered_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rendered_image_rgb)

    df = results.pandas().xyxy[0]  

    regions = []

    original_image = Image.open(image_path).convert("RGB")

    # Iterate through detections
    for index, row in df.iterrows():
        # Extract bounding box coordinates
        xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        # Crop region
        region = original_image.crop((xmin, ymin, xmax, ymax))

        # Append to the list
        regions.append(region)

    return pil_image, df, regions