import torch
from models.yolo import Model

import os
import sys
import pathlib

sys.modules["pathlib._local"] = pathlib 
if os.name == 'nt':
   pathlib.PosixPath = pathlib.WindowsPath
else:
   pathlib.WindowsPath = pathlib.PosixPath
   
cfg = 'models/yolov5x.yaml'  # или твой кастомный .yaml, если был другой
nc = 15  # укажи правильное количество классов (то, что было при обучении)

# Создать новую модель с нуля
model = Model(cfg, ch=3, nc=nc)

# Загрузить только веса
weights = torch.load('runs/train/exp2/weights/best.pt', map_location='cpu')
model.load_state_dict(weights)

# Включить режим оценки
model.eval()

print('Модель успешно загружена с весами.')