# WildGuard - AI Wildlife Detection & Road Safety System

An advanced computer vision system that detects wildlife on roadways and assesses collision risks in real-time.

## Features

- Real-time animal detection using YOLOv8
- Dynamic risk assessment based on animal proximity to road
- Speed-aware collision probability calculation
- Billboard alert generation for safety warnings
- Web-based Gradio interface for easy interaction
- Comprehensive testing suite included

## Installation

### Quick Setup
\`\`\`bash
python scripts/setup_environment.py
\`\`\`

### Manual Installation
\`\`\`bash
pip install ultralytics==8.0.228 gradio==4.41.1 opencv-python-headless pillow numpy
\`\`\`

## Usage

### 1. Prepare Environment
\`\`\`bash
python scripts/setup_environment.py
\`\`\`

### 2. Generate Test Data
\`\`\`bash
python scripts/generate_test_data.py
\`\`\`

### 3. Run Tests
\`\`\`bash
python scripts/test_wildguard.py
\`\`\`

### 4. Launch Web Interface
\`\`\`bash
python wildguard_detector.py
\`\`\`

Then open the URL displayed in your browser (typically http://localhost:7860)

## System Components

### WildGuardDetector
Detects animals in images using YOLOv8 model.
- Supports 10+ animal species
- Configurable confidence threshold
- Fast inference speed

### RiskAssessor
Evaluates collision risk based on:
- Distance from road
- Vehicle speed
- Animal crossing probability
- Dynamic risk scoring (0.0 - 1.0)

### BillboardGenerator
Creates safety alerts with:
- Risk-level indicators (CRITICAL, WARNING, CAUTION, LOW)
- Dynamic speed recommendations
- Timestamp logging

## Data Format

### Detection Output
\`\`\`
{
  'bbox': [x1, y1, x2, y2],
  'class': 'dog',
  'confidence': 0.95,
  'class_id': 14
}
\`\`\`

### Risk Assessment Output
\`\`\`
{
  'risk_score': 0.85,
  'alert_level': 'WARNING',
  'crossing_probability': 0.75,
  'distance_to_road': 0.15
}
\`\`\`

## Testing

Run the complete test suite:
\`\`\`bash
python scripts/test_wildguard.py
\`\`\`

This includes:
- Risk assessment validation
- Alert generation testing
- Synthetic data creation
- End-to-end integration tests
- Performance metrics

## Performance

- Risk Assessment: ~0.2ms per animal
- Alert Generation: ~0.1ms per alert
- Full Image Processing: ~1-2s (depends on image size and detections)

## Supported Animals

- Dog
- Cat
- Bird
- Horse
- Sheep
- Cow
- Elephant
- Bear
- Zebra
- Giraffe

## Alert Levels

- **CRITICAL**: Animal on road (Risk > 0.7)
- **WARNING**: Animal very close to road (Risk 0.5-0.7)
- **CAUTION**: Animal approaching road (Risk 0.3-0.5)
- **LOW**: Animal far from road (Risk < 0.3)

## Project Structure

\`\`\`
wildguard/
├── wildguard_detector.py       # Main detection system
├── scripts/
│   ├── setup_environment.py    # Environment setup
│   ├── generate_test_data.py   # Test data generator
│   ├── test_wildguard.py       # Test suite
│   └── demo_runner.py          # Demo runner
├── test_images/                # Test data directory
├── outputs/                    # Processing results
└── README.md                   # This file
\`\`\`

## API Usage

\`\`\`python
from wildguard_detector import process_wildlife_image
from PIL import Image

# Load image
image = Image.open('wildlife.jpg')

# Process
result_img, details, alerts = process_wildlife_image(image, vehicle_speed=60)
\`\`\`

## Troubleshooting

**Issue**: YOLOv8 model download fails
- Solution: Check internet connection, manually download model

**Issue**: Gradio interface won't launch
- Solution: Ensure port 7860 is available

**Issue**: Low detection accuracy
- Solution: Ensure images are clear and well-lit

## Future Enhancements

- Multi-frame video processing
- Real-time camera streaming
- Custom model fine-tuning
- Mobile app integration
- Advanced trajectory prediction

## License

Open source - Available for research and educational purposes

## Support

For issues or questions, refer to the test suite output for diagnostic information.
