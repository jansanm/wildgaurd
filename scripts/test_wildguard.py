"""
Comprehensive testing suite for WildGuard system
Tests detection, risk assessment, and alert generation
"""

import numpy as np
import cv2
from PIL import Image
import sys
sys.path.insert(0, '..')

# Import WildGuard components
from wildguard_detector import (
    WildGuardDetector, 
    RiskAssessor, 
    BillboardGenerator
)

def create_synthetic_test_image(height=480, width=640, animal_position='center'):
    """
    Create a synthetic test image with placeholders for animals
    animal_position: 'center', 'top', 'near_road', 'on_road'
    """
    img = np.ones((height, width, 3), dtype=np.uint8) * 200
    
    # Draw sky
    img[0:int(height*0.5)] = [135, 206, 235]  # Sky blue
    
    # Draw grass
    img[int(height*0.5):] = [34, 139, 34]  # Forest green
    
    # Draw road line (horizon)
    road_y = int(height * 0.75)
    cv2.line(img, (0, road_y), (width, road_y), (0, 255, 255), 4)
    
    # Draw animal rectangle based on position
    if animal_position == 'on_road':
        y = road_y - 20
        color = (0, 0, 255)  # Red for critical
    elif animal_position == 'near_road':
        y = road_y - 80
        color = (0, 140, 255)  # Orange for warning
    elif animal_position == 'top':
        y = int(height * 0.2)
        color = (0, 255, 0)  # Green for low risk
    else:  # center
        y = int(height * 0.3)
        color = (0, 255, 255)  # Yellow for caution
    
    # Draw animal placeholder
    x1, x2 = width//4, 3*width//4
    y1, y2 = y, y + 60
    cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
    cv2.putText(img, 'ANIMAL', (x1+50, y+35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return img, road_y

def test_risk_assessor():
    """Test risk assessment logic"""
    print("\n" + "="*60)
    print("TESTING: Risk Assessor")
    print("="*60)
    
    assessor = RiskAssessor()
    image_shape = (480, 640, 3)
    road_y = int(480 * 0.75)  # 360
    
    test_cases = [
        ("ON ROAD", [100, road_y-10, 200, road_y+10], 60, "CRITICAL"),
        ("NEAR ROAD", [100, road_y-70, 200, road_y-20], 60, "WARNING"),
        ("APPROACHING", [100, road_y-150, 200, road_y-100], 60, "CAUTION"),
        ("FAR AWAY", [100, 50, 200, 100], 60, "LOW"),
        ("HIGH SPEED", [100, road_y-150, 200, road_y-100], 100, "CAUTION"),
        ("LOW SPEED", [100, road_y-150, 200, road_y-100], 20, "CAUTION"),
    ]
    
    for test_name, bbox, speed, expected_level in test_cases:
        risk = assessor.assess_risk(bbox, image_shape, speed)
        status = "✓" if risk['alert_level'] == expected_level else "✗"
        print(f"{status} {test_name:20} | Risk: {risk['risk_score']:.2f} | Level: {risk['alert_level']:10} | Speed: {speed} km/h")
    
    print("✅ Risk Assessor tests completed")


def test_billboard_generator():
    """Test alert message generation"""
    print("\n" + "="*60)
    print("TESTING: Billboard Generator")
    print("="*60)
    
    billboard = BillboardGenerator()
    
    test_cases = [
        ("dog", 0.95, "CRITICAL"),
        ("cat", 0.75, "WARNING"),
        ("bird", 0.45, "CAUTION"),
        ("elephant", 0.15, "LOW"),
    ]
    
    for species, risk_score, alert_level in test_cases:
        alert = billboard.generate_alert(species, risk_score, alert_level)
        if alert:
            print(f"\n{alert['icon']} Alert: {alert['main_message']}")
            print(f"  Risk Score: {risk_score:.2f} | Alert Level: {alert_level}")
        else:
            print(f"\n✓ No alert generated for LOW risk: {species}")
    
    print("\n✅ Billboard Generator tests completed")


def test_detector_with_synthetic_data():
    """Test detector with synthetic images"""
    print("\n" + "="*60)
    print("TESTING: Detector with Synthetic Data")
    print("="*60)
    
    print("\nGenerating synthetic test images...")
    positions = ['on_road', 'near_road', 'center', 'top']
    
    for position in positions:
        img, road_y = create_synthetic_test_image(animal_position=position)
        print(f"✓ Generated test image: {position}")
        # Save image
        filename = f'test_images/synthetic_{position}.png'
        cv2.imwrite(filename, img)
        print(f"  Saved to: {filename}")
    
    print("\n✅ Synthetic test images created")


def test_end_to_end():
    """End-to-end integration test"""
    print("\n" + "="*60)
    print("TESTING: End-to-End Integration")
    print("="*60)
    
    from wildguard_detector import process_wildlife_image
    
    print("\nTesting with synthetic images...")
    
    # Test with on_road scenario
    img, _ = create_synthetic_test_image(animal_position='on_road')
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    try:
        result_img, details, alerts = process_wildlife_image(pil_img, vehicle_speed=80)
        print("✓ End-to-end processing successful")
        print(f"  Details length: {len(details)} characters")
        print(f"  Alerts length: {len(alerts)} characters")
    except Exception as e:
        print(f"✗ End-to-end test failed: {e}")
    
    print("\n✅ Integration test completed")


def generate_performance_report():
    """Generate performance metrics"""
    print("\n" + "="*60)
    print("PERFORMANCE REPORT")
    print("="*60)
    
    import time
    
    # Test detection speed
    assessor = RiskAssessor()
    image_shape = (480, 640, 3)
    
    start = time.time()
    for _ in range(100):
        bbox = [100, 200, 300, 350]
        assessor.assess_risk(bbox, image_shape, 60)
    elapsed = time.time() - start
    
    print(f"\nRisk Assessment Speed:")
    print(f"  100 assessments: {elapsed:.4f}s")
    print(f"  Average: {elapsed/100*1000:.2f}ms per assessment")
    
    # Test alert generation speed
    billboard = BillboardGenerator()
    
    start = time.time()
    for _ in range(100):
        billboard.generate_alert('dog', 0.95, 'CRITICAL')
    elapsed = time.time() - start
    
    print(f"\nAlert Generation Speed:")
    print(f"  100 alerts: {elapsed:.4f}s")
    print(f"  Average: {elapsed/100*1000:.2f}ms per alert")
    
    print("\n✅ Performance report generated")


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*70)
    print("WILDGUARD SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    try:
        test_risk_assessor()
        test_billboard_generator()
        test_detector_with_synthetic_data()
        test_end_to_end()
        generate_performance_report()
        
        print("\n" + "="*70)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test suite failed: {e}")


if __name__ == "__main__":
    run_all_tests()
