from pathlib import Path
import os
import cv2
import numpy as np

ROI_PATH = Path(r'C:\Projects\MastersThesis\HMICutter\ROI_EXT')
SOURCE_PATH = Path(r'C:\Projects\MastersThesis\HMICutter\Source')

def get_range(threshold, sigma=0.33):
    return int((1 - sigma) * threshold), int((1 + sigma) * threshold)

def param(gray, background="gray", canny=True, threshtype="triangle"):
    # Blur configuration
    blur = cv2.GaussianBlur(gray, (5, 5), 0) if background == "white" else cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding or edge detection
    if not canny:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 2) if background == "white" else (1, 1))
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    else:
        if threshtype == "otsu":
            val, _ = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)
        elif threshtype == "triangle":
            val, _ = cv2.threshold(blur, 0, 255, cv2.THRESH_TRIANGLE)
        elif threshtype == "manual":
            val = np.median(blur)
        else:
            raise ValueError(f"Unsupported threshold type: {threshtype}")

        thresh = cv2.Canny(blur, *get_range(val))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))

    return thresh, kernel

# Main loop
for image_path in SOURCE_PATH.iterdir():
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Warning: Could not read {image_path}")
        continue

    original = image.copy()
    name = f"lib_{image_path.stem}"

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, kernel = param(gray)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # Show filtered image
    cv2.imshow("Filtered (Threshold/Canny)", thresh)
    cv2.waitKey(0)

    # Find and draw contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if w > 14 and h > 14:
            ROI = original[y:y+h, x:x+w]
            save_path = ROI_PATH / f"{name}_ROI_{idx}.png"
            if not cv2.imwrite(str(save_path), ROI):
                raise IOError(f"Failed to save image: {save_path}")
            cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)

    # Show image with contours
    cv2.imshow("Detected Contours", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()