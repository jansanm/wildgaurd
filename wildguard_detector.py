# ═══════════════════════════════════════════════════════════════
# WildGuard - AI Wildlife Detection & Road Safety System
# Fixed and Enhanced Version with Proper Bug Fixes
# ═══════════════════════════════════════════════════════════════

import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import gradio as gr
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("🚀 Initializing WildGuard System...")

# ═══════════════════════════════════════════════════════════════
# ANIMAL DETECTOR - YOLOv8 Based
# ═══════════════════════════════════════════════════════════════

class WildGuardDetector:
    def __init__(self):
        print("📥 Loading YOLOv8 model...")
        self.model = YOLO('yolov8n.pt')
        # COCO dataset animal classes
        self.animal_classes = {
            14: 'dog', 15: 'cat', 16: 'bird', 17: 'horse',
            18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear',
            22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella'
        }
        print("✅ Model loaded successfully!")
    
    def detect(self, image):
        """
        Fixed bounding box extraction logic - properly unpacks coordinates
        """
        try:
            results = self.model(image, conf=0.25, verbose=False)
            detections = []
            
            if results and len(results) > 0:
                result = results[0]  # Get first result properly
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        xyxy = box.xyxy[0].cpu().numpy()
                        x1, y1, x2, y2 = float(xyxy[0]), float(xyxy[1]), float(xyxy[2]), float(xyxy[3])
                        conf = float(box.conf.cpu().numpy()[0])
                        cls = int(box.cls.cpu().numpy()[0])
                        
                        if cls in self.animal_classes:
                            detections.append({
                                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                                'class': self.animal_classes[cls],
                                'confidence': conf,
                                'class_id': cls
                            })
            
            return detections
        except Exception as e:
            print(f"Detection error: {e}")
            return []


# ═══════════════════════════════════════════════════════════════
# RISK ASSESSOR - Collision Risk Analysis
# ═══════════════════════════════════════════════════════════════

class RiskAssessor:
    def assess_risk(self, bbox, image_shape, vehicle_speed=60):
        """
        Fixed center_y calculation - was using bbox+bbox incorrectly
        """
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


# ═══════════════════════════════════════════════════════════════
# BILLBOARD GENERATOR - Alert Messages
# ═══════════════════════════════════════════════════════════════

class BillboardGenerator:
    def generate_alert(self, species, risk_score, alert_level):
        if alert_level == "LOW":
            return None
        
        icons = {
            'CRITICAL': '🚨',
            'WARNING': '⚠️',
            'CAUTION': 'ℹ️'
        }
        messages = {
            'CRITICAL': f"DANGER: {species.upper()} ON ROAD!",
            'WARNING': f"CAUTION: {species.upper()} DETECTED",
            'CAUTION': f"Wildlife Alert: {species.upper()}"
        }
        
        return {
            'icon': icons.get(alert_level, 'ℹ️'),
            'main_message': messages.get(alert_level, 'Alert'),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }


# ═══════════════════════════════════════════════════════════════
# INITIALIZE SYSTEMS
# ═══════════════════════════════════════════════════════════════

detector = WildGuardDetector()
assessor = RiskAssessor()
billboard = BillboardGenerator()

print("✅ All detection systems initialized!\n")


# ═══════════════════════════════════════════════════════════════
# MAIN PROCESSING FUNCTION
# ═══════════════════════════════════════════════════════════════

def process_wildlife_image(image, vehicle_speed=60):
    """
    Process wildlife image and return detection results with risk assessment
    """
    try:
        if image is None:
            return None, "No image provided", "No alerts"
        
        # Convert PIL to numpy if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Handle grayscale
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
        # Handle RGBA
        if image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        h, w = image_bgr.shape[:2]
        
        # Detect animals
        detections = detector.detect(image_bgr)
        
        if len(detections) == 0:
            output = image_bgr.copy()
            cv2.putText(output, "No animals detected", (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
            output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
            return output_rgb, "No animals detected", "No alerts"
        
        # Process detections
        output = image_bgr.copy()
        results_text = f"Detected {len(detections)} animal(s)\n\n"
        billboard_alerts = []
        
        # Draw road line
        road_y = int(h * 0.75)
        cv2.line(output, (0, road_y), (w, road_y), (0, 255, 255), 3)
        cv2.putText(output, "ROAD LINE", (w//2 - 80, road_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Process each detection
        for idx, det in enumerate(detections):
            risk = assessor.assess_risk(det['bbox'], image_bgr.shape, vehicle_speed)
            
            x1, y1, x2, y2 = det['bbox']
            
            # Color coding based on risk
            if risk['risk_score'] > 0.7:
                color = (0, 0, 255)  # Red - Critical
            elif risk['risk_score'] > 0.5:
                color = (0, 140, 255)  # Orange - Warning
            elif risk['risk_score'] > 0.3:
                color = (0, 255, 255)  # Yellow - Caution
            else:
                color = (0, 255, 0)  # Green - Low
            
            # Draw bounding box
            cv2.rectangle(output, (x1, y1), (x2, y2), color, 4)
            
            # Draw info box
            cv2.rectangle(output, (x1, y1 - 90), (x2, y1), (0, 0, 0), -1)
            
            # Write info
            y_offset = y1 - 70
            cv2.putText(output, det['class'].upper(), (x1 + 5, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            y_offset += 25
            cv2.putText(output, f"Conf: {det['confidence']:.0%}", (x1 + 5, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 20
            cv2.putText(output, f"Cross: {risk['crossing_probability']:.0%}", (x1 + 5, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 20
            cv2.putText(output, f"Risk: {risk['risk_score']:.2f}", (x1 + 5, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Build results text
            results_text += f"Detection #{idx + 1}: {det['class'].upper()}\n"
            results_text += f"  Confidence: {det['confidence']:.1%}\n"
            results_text += f"  Crossing Probability: {risk['crossing_probability']:.1%}\n"
            results_text += f"  Risk Score: {risk['risk_score']:.2f}/1.0\n"
            results_text += f"  Alert Level: {risk['alert_level']}\n"
            results_text += f"  Distance to Road: {risk['distance_to_road']:.2%}\n\n"
            
            # Billboard alert
            alert = billboard.generate_alert(det['class'], risk['risk_score'], risk['alert_level'])
            if alert:
                billboard_msg = f"{alert['icon']} {alert['main_message']}\n"
                billboard_msg += f"   Species: {det['class'].upper()}\n"
                billboard_msg += f"   Risk Score: {risk['risk_score']:.2f}\n"
                billboard_msg += f"   Crossing Prob: {risk['crossing_probability']:.0%}\n"
                billboard_msg += f"   Recommended Speed: 40 km/h\n"
                billboard_msg += f"   Time: {alert['timestamp']}\n"
                billboard_alerts.append(billboard_msg)
        
        # Convert back to RGB for display
        output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        
        if billboard_alerts:
            billboard_text = "BILLBOARD ALERTS:\n\n" + "\n---\n\n".join(billboard_alerts)
        else:
            billboard_text = "No alerts (low risk)"
        
        return output_rgb, results_text, billboard_text
        
    except Exception as e:
        return image if image is not None else None, f"Error: {str(e)}", "Error"


# ═══════════════════════════════════════════════════════════════
# CREATE GRADIO INTERFACE
# ═══════════════════════════════════════════════════════════════

print("Creating Gradio interface...")

interface = gr.Interface(
    fn=process_wildlife_image,
    inputs=[
        gr.Image(type="pil", label="Upload Wildlife Image"),
        gr.Slider(0, 120, 60, step=5, label="Vehicle Speed (km/h)")
    ],
    outputs=[
        gr.Image(type="numpy", label="Detection Result"),
        gr.Textbox(label="Detection Details", lines=15),
        gr.Textbox(label="Billboard Alerts", lines=10)
    ],
    title="WildGuard - AI Wildlife Detection & Road Safety System",
    description="Upload wildlife images to detect animals, predict crossing behavior, and generate safety alerts.",
    examples=[],
    theme=gr.themes.Soft()
)

print("✅ Interface created!\n")

# ═══════════════════════════════════════════════════════════════
# LAUNCH SYSTEM
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("LAUNCHING WILDGUARD SYSTEM")
    print("=" * 60 + "\n")
    interface.launch(share=True)
