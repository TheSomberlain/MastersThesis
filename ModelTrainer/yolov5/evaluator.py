import torch
import pathlib
import os
import sys
sys.modules["pathlib._local"] = pathlib 
if os.name == 'nt':
   pathlib.PosixPath = pathlib.WindowsPath
else:
   pathlib.WindowsPath = pathlib.PosixPath

from pathlib import Path

path = Path('runs/train/exp2/weights/best.pt').resolve()

model = torch.hub.load('', 'custom', path=str(path), source='local', force_reload=True)
model.conf = 0.3 
model.iou = 0.35  

results = model('../test/sugar_15.png')

results.print()
results.show()