"""
Generate synthetic wildlife detection test data for WildGuard
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_animal_test_image(animal_name, width=640, height=480):
    """
    Create a test image with text representation of an animal
    """
    img = Image.new('RGB', (width, height), color=(200, 220, 255))
    draw = ImageDraw.Draw(img)
    
    # Add animal name
    text_bbox = draw.textbbox((0, 0), animal_name.upper())
    text_x = (width - (text_bbox[2] - text_bbox[0])) // 2
    text_y = height // 3
    draw.text((text_x, text_y), animal_name.upper(), fill=(0, 0, 0))
    
    # Add road line
    road_y = int(height * 0.75)
    draw.line([(0, road_y), (width, road_y)], fill=(255, 255, 0), width=3)
    draw.text((width//2 - 50, road_y + 10), "ROAD", fill=(255, 255, 0))
    
    # Add safety distance zones
    # Critical zone (red)
    draw.rectangle([(0, road_y - 30), (width, road_y + 30)], 
                   outline=(0, 0, 255), width=2)
    draw.text((10, road_y - 25), "CRITICAL ZONE", fill=(0, 0, 255))
    
    # Warning zone (orange)
    draw.rectangle([(0, road_y - 80), (width, road_y + 80)], 
                   outline=(0, 140, 255), width=2)
    draw.text((10, road_y - 75), "WARNING ZONE", fill=(0, 140, 255))
    
    # Caution zone (yellow)
    draw.rectangle([(0, road_y - 150), (width, road_y + 150)], 
                   outline=(0, 255, 255), width=2)
    draw.text((10, road_y - 145), "CAUTION ZONE", fill=(0, 255, 255))
    
    return np.array(img)


def create_test_dataset():
    """
    Create test images directory with wildlife examples
    """
    os.makedirs('test_images', exist_ok=True)
    
    animals = ['dog', 'cat', 'bird', 'deer', 'cow', 'horse', 'elephant', 'bear']
    
    print("Generating test images...")
    for animal in animals:
        img = create_animal_test_image(animal)
        path = f'test_images/{animal}_test.png'
        cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(f"  Created: {path}")
    
    print("✅ Test dataset created in 'test_images/' directory")


if __name__ == "__main__":
    create_test_dataset()
