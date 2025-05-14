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
    # Предсказание
    results = model(image_path)

    # Получаем DataFrame
    df = results.pandas().xyxy[0]

    # Открываем оригинал как OpenCV для рисования
    image_cv = cv2.imread(image_path)
    
    # Проходимся по предсказаниям
    for _, row in df.iterrows():
        xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        label = row['name']
        
        # Рисуем тонкую рамку (зеленая)
        cv2.rectangle(image_cv, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        
        # Пишем только имя класса
        cv2.putText(image_cv, label, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2, cv2.LINE_AA)

    # Переводим в RGB для PIL
    image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)

    # Также выделяем регионы (из PIL оригинала)
    original_image = Image.open(image_path).convert("RGB")
    regions = []
    for _, row in df.iterrows():
        xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        label = row['name']
        region = original_image.crop((xmin, ymin, xmax, ymax))
        regions.append({
            'image': region,
            'label': label,
            'xmin': xmin,
            'ymin': ymin,
            'xmax': xmax,
            'ymax': ymax,
        })

    return pil_image, df, regions