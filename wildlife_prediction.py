import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
import os
import requests
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

MODEL_NAME = 'yolov8n.pt'  # Using nano model for speed in demo
SAMPLE_IMAGE_URL = "https://images.unsplash.com/photo-1551266519-ddbf97b26fde"
SAMPLE_IMAGE_PATH = "deer_sample.jpg"
OUTPUT_PATH = "prediction_output.jpg"

# ═══════════════════════════════════════════════════════════════
# RISK ASSESSOR
# ═══════════════════════════════════════════════════════════════

class RiskAssessor:
    def assess_risk(self, bbox, image_shape):
        """
        Calculates risk based on the animal's position relative to a virtual road.
        """
        h, w = image_shape[:2]
        x1, y1, x2, y2 = bbox
        
        # Calculate bottom center of the bounding box (animal's "feet")
        feet_y = y2
        
        # Define virtual road line (e.g., at 75% of image height)
        road_y = h * 0.75
        
        # Calculate normalized distance to road (0.0 = on road, 1.0 = top of image)
        # We use signed distance: positive means above road, negative means on/below road
        distance_pixels = road_y - feet_y
        distance_norm = distance_pixels / h
        
        # Determine risk level
        if distance_norm < 0.05: # Very close or on road
            risk_score = 0.95
            alert_level = "CRITICAL"
            crossing_prob = 0.98
        elif distance_norm < 0.15: # Approaching
            risk_score = 0.75
            alert_level = "WARNING"
            crossing_prob = 0.80
        elif distance_norm < 0.30: # Nearby
            risk_score = 0.45
            alert_level = "CAUTION"
            crossing_prob = 0.40
        else: # Far away
            risk_score = 0.15
            alert_level = "LOW"
            crossing_prob = 0.10
            
        return {
            'risk_score': risk_score,
            'alert_level': alert_level,
            'crossing_probability': crossing_prob,
            'distance_norm': distance_norm,
            'road_y': int(road_y)
        }

# ═══════════════════════════════════════════════════════════════
# BILLBOARD GENERATOR
# ═══════════════════════════════════════════════════════════════

class BillboardGenerator:
    def generate_alert(self, species, risk_data):
        """
        Generates the text content for the billboard.
        """
        alert_level = risk_data['alert_level']
        
        if alert_level == "LOW":
            return None
        
        icons = {
            'CRITICAL': '🚨',
            'WARNING': '⚠️',
            'CAUTION': 'ℹ️'
        }
        
        headlines = {
            'CRITICAL': "STOP! ANIMAL CROSSING",
            'WARNING': "SLOW DOWN - WILDLIFE",
            'CAUTION': "DRIVE WITH CARE"
        }
        
        return {
            'icon': icons.get(alert_level, 'ℹ️'),
            'headline': headlines.get(alert_level, 'WILDLIFE ALERT'),
            'subtext': f"{species.upper()} DETECTED",
            'risk_score': risk_data['risk_score'],
            'color': self._get_color(alert_level)
        }
    
    def _get_color(self, alert_level):
        if alert_level == 'CRITICAL': return (0, 0, 255)      # Red
        if alert_level == 'WARNING': return (0, 165, 255)     # Orange
        if alert_level == 'CAUTION': return (0, 255, 255)     # Yellow
        return (0, 255, 0)                                    # Green

# ═══════════════════════════════════════════════════════════════
# MAIN WORKFLOW
# ═══════════════════════════════════════════════════════════════

def main():
    print("🚀 Starting WildGuard Crossing Prediction System...")

    # 1. Setup Data
    if not os.path.exists(SAMPLE_IMAGE_PATH):
        print("🔽 Downloading sample image...")
        response = requests.get(SAMPLE_IMAGE_URL)
        with open(SAMPLE_IMAGE_PATH, 'wb') as f:
            f.write(response.content)
    
    # 2. Load Model
    print("🧠 Loading YOLOv8 model...")
    model = YOLO(MODEL_NAME)
    
    # 3. Read Image
    print(f"📸 Processing {SAMPLE_IMAGE_PATH}...")
    img = cv2.imread(SAMPLE_IMAGE_PATH)
    if img is None:
        print("❌ Error: Could not read image.")
        return

    # 4. Run Detection
    results = model.predict(source=img, conf=0.4, save=False, verbose=False)
    
    # 5. Process Results
    assessor = RiskAssessor()
    billboard = BillboardGenerator()
    
    output_img = img.copy()
    h, w = output_img.shape[:2]
    
    # Draw Road Line
    road_y = int(h * 0.75)
    cv2.line(output_img, (0, road_y), (w, road_y), (255, 255, 255), 2)
    cv2.putText(output_img, "VIRTUAL ROAD LINE", (10, road_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    highest_risk_alert = None
    
    if len(results[0].boxes) > 0:
        print(f"📊 Found {len(results[0].boxes)} objects.")
        
        for box in results[0].boxes:
            # Get box info
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]
            
            # Assess Risk
            risk_data = assessor.assess_risk([x1, y1, x2, y2], img.shape)
            
            # Generate Alert
            alert = billboard.generate_alert(class_name, risk_data)
            
            # Track highest risk for the main billboard
            if alert:
                if highest_risk_alert is None or alert['risk_score'] > highest_risk_alert['risk_score']:
                    highest_risk_alert = alert

            # Draw Bounding Box & Info
            color = billboard._get_color(risk_data['alert_level'])
            cv2.rectangle(output_img, (x1, y1), (x2, y2), color, 2)
            
            label = f"{class_name.upper()} | Risk: {risk_data['risk_score']:.2f}"
            cv2.putText(output_img, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # 6. Draw Billboard
    if highest_risk_alert:
        # Create a semi-transparent overlay for the billboard
        overlay = output_img.copy()
        
        # Billboard dimensions
        bb_w, bb_h = 400, 150
        bb_x, bb_y = w - bb_w - 20, 20
        
        cv2.rectangle(overlay, (bb_x, bb_y), (bb_x + bb_w, bb_y + bb_h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, output_img, 0.3, 0, output_img)
        
        # Border
        cv2.rectangle(output_img, (bb_x, bb_y), (bb_x + bb_w, bb_y + bb_h), highest_risk_alert['color'], 3)
        
        # Text
        cv2.putText(output_img, highest_risk_alert['icon'], (bb_x + 20, bb_y + 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 3)
        
        cv2.putText(output_img, highest_risk_alert['headline'], (bb_x + 90, bb_y + 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, highest_risk_alert['color'], 2)
        
        cv2.putText(output_img, highest_risk_alert['subtext'], (bb_x + 90, bb_y + 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.putText(output_img, "PREDICTED CROSSING", (bb_x + 90, bb_y + 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        print(f"⚠️ BILLBOARD ACTIVATED: {highest_risk_alert['headline']}")
    else:
        print("✅ No high-risk animals detected.")

    # 7. Save Output
    cv2.imwrite(OUTPUT_PATH, output_img)
    print(f"💾 Result saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
