from ultralytics import YOLO
import cv2

# Load model
model = YOLO('/Users/quanteondev/Downloads/wildlife-/yolov8m.pt')

# Image path
img_path = '/Users/quanteondev/Downloads/wildlife-/dog.jpg'

# Predict
results = model(img_path, conf=0.05)

print("\n--- DETECTIONS ---")
for result in results:
    for box in result.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        name = result.names[cls_id]
        print(f"Class: {name}, ID: {cls_id}, Conf: {conf:.2f}")
print("------------------\n")
