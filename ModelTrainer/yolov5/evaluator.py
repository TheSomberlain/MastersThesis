import torch
import pathlib
import os
import sys
import cv2
sys.modules["pathlib._local"] = pathlib 
if os.name == 'nt':
   pathlib.PosixPath = pathlib.WindowsPath
else:
   pathlib.WindowsPath = pathlib.PosixPath

from pathlib import Path

def draw_yolo_torchhub_custom(image_path, model, save_path='result_custom.jpg', box_color=(0, 255, 0), box_thickness=2, font_scale=0.75, font_thickness=2, conf_threshold=0.25):
    image = cv2.imread(image_path)
    results = model(image)

    df = results.pandas().xyxy[0]

    for _, row in df.iterrows():
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        label = row['name']

        cv2.rectangle(image, (x1, y1), (x2, y2), box_color, box_thickness)

        cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, box_color, font_thickness, cv2.LINE_AA)

    cv2.imwrite(save_path, image)
    print(f'✅ Результат сохранён: {save_path}')

path = Path('runs/train/exp2/weights/best.pt').resolve()

model = torch.hub.load('', 'custom', path=str(path), source='local', force_reload=True)
model.conf = 0.3 
model.iou = 0.35  

draw_yolo_torchhub_custom(
    image_path='../test/sugar_15.png',
    model=model,
)