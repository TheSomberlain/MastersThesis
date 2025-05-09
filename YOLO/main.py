import torch

# Load the model (from local path)
model = torch.hub.load('yolov5', 'custom', path='yolov5/runs/train/exp8/weights/best.pt', source='local')

# Run inference
results = model(r'C:\Projects\MastersThesis\YOLO\test\operator-interface.png')
model.conf=0.5

# Show and save results
results.print()
results.show()
