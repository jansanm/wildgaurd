import sys
import json
import cv2
import numpy as np
from ultralytics import YOLO

# Initialize model
# Using absolute path to be safe, or relative to the script location
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'yolov8m.pt')

try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(json.dumps({"error": f"Failed to load model: {str(e)}"}))
    sys.exit(1)

class RiskAssessor:
    def assess_risk(self, bbox, image_shape, vehicle_speed=60):
        h, w = image_shape[:2]
        x1, y1, x2, y2 = bbox
        center_y = (y1 + y2) / 2
        road_y = h * 0.75  # Road assumed at 75% of image height
        
        distance_to_road = abs(center_y - road_y) / h
        
        # Risk scoring based on distance
        if distance_to_road < 0.05:
            risk_score = 0.95
            alert_level = "CRITICAL"
            crossing_prob = 0.98
        elif distance_to_road < 0.15:
            risk_score = 0.75
            alert_level = "WARNING"
            crossing_prob = 0.80
        elif distance_to_road < 0.35:
            risk_score = 0.45
            alert_level = "CAUTION"
            crossing_prob = 0.50
        else:
            risk_score = 0.15
            alert_level = "LOW"
            crossing_prob = 0.20
        
        # Speed factor adjustment
        speed_factor = min(vehicle_speed / 100, 1.0)
        risk_score = min(risk_score * (1 + speed_factor * 0.5), 1.0)
        
        return {
            'risk_score': risk_score,
            'alert_level': alert_level,
            'crossing_probability': crossing_prob,
            'distance_to_road': distance_to_road
        }

def normalize_animal_name(name):
    return name.replace('_', ' ').title()

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No image path provided"}))
        sys.exit(1)
        
    img_path = sys.argv[1]
    
    try:
        # Read image
        image = cv2.imread(img_path)
        if image is None:
            print(json.dumps({"error": "Could not read image"}))
            sys.exit(1)
            
        # Detect
        results = model(image, conf=0.25, verbose=False)
        
        detections_list = []
        max_risk_score = 0
        max_crossing_prob = 0
        min_distance_to_road = 1.0
        overall_alert_level = "safe"
        
        assessor = RiskAssessor()
        
        if results and len(results) > 0:
            result = results[0]
            if result.boxes is not None:
                for idx, box in enumerate(result.boxes):
                    xyxy = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = float(xyxy[0]), float(xyxy[1]), float(xyxy[2]), float(xyxy[3])
                    conf = float(box.conf.cpu().numpy()[0])
                    cls = int(box.cls.cpu().numpy()[0])
                    class_name = result.names[cls]
                    
                    # Calculate bbox for frontend (x, y, width, height)
                    bbox_width = x2 - x1
                    bbox_height = y2 - y1
                    
                    # Assess risk
                    risk = assessor.assess_risk([x1, y1, x2, y2], image.shape)
                    
                    detections_list.append({
                        "id": idx,
                        "animal": normalize_animal_name(class_name),
                        "confidence": round(conf * 100, 1),
                        "bbox": {
                            "x": int(x1),
                            "y": int(y1),
                            "width": int(bbox_width),
                            "height": int(bbox_height)
                        },
                        "risk": risk
                    })
                    
                    # Update aggregate stats
                    if risk['risk_score'] > max_risk_score:
                        max_risk_score = risk['risk_score']
                        overall_alert_level = risk['alert_level'].lower()
                    
                    max_crossing_prob = max(max_crossing_prob, risk['crossing_probability'])
                    min_distance_to_road = min(min_distance_to_road, risk['distance_to_road'])

        # Map alert level to frontend expected values
        if overall_alert_level == "critical":
            risk_level = "critical"
        elif overall_alert_level == "warning":
            risk_level = "warning"
        elif overall_alert_level == "caution":
            risk_level = "caution"
        else:
            risk_level = "safe"

        output = {
            "detections": detections_list,
            "vehicleSpeed": 65, # Default or passed in args
            "riskLevel": risk_level,
            "crossingProbability": round(max_crossing_prob * 100),
            "distanceToRoad": round(min_distance_to_road * 100) # Frontend expects percentage or value? TS says `distanceToRoad: hasHighRiskAnimal ? 8 : 25`. It seems to be meters or arbitrary units. Python gives 0.0-1.0. Let's convert to something reasonable. 
            # If 0.05 (close) -> maybe 5 meters. If 0.5 (far) -> 50 meters.
            # Let's just multiply by 100 for now to give a "distance" value.
        }
        
        print(json.dumps(output))
        
    except Exception as e:
        print(json.dumps({"error": f"Processing error: {str(e)}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
