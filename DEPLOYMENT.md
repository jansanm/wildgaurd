# WildGuard Deployment Guide

## Local Deployment

### Step 1: Clone & Setup
\`\`\`bash
# Clone or download the project
cd wildguard

# Install dependencies
python scripts/setup_environment.py

# Generate test data
python scripts/generate_test_data.py
\`\`\`

### Step 2: Run Tests
\`\`\`bash
python scripts/test_wildguard.py
\`\`\`

Expected output:
- Risk Assessor tests: All ✓
- Billboard Generator tests: All ✓
- Synthetic images created
- End-to-end integration: Successful

### Step 3: Launch Interface
```bash
python wildguard_detector.py
```

Access at: http://localhost:7860

## Docker Deployment

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 7860

# Run application
CMD ["python", "wildguard_detector.py"]
```

### Step 2: Build & Run
```bash
# Build image
docker build -t wildguard:latest .

# Run container
docker run -p 7860:7860 wildguard:latest
```

Access at: http://localhost:7860

## Cloud Deployment Options

### Option 1: HuggingFace Spaces
1. Create Space at https://huggingface.co/spaces
2. Choose "Docker" runtime
3. Upload Dockerfile and files
4. HuggingFace handles deployment

### Option 2: AWS Lambda
Uses Gradio's built-in deployment:
```python
# In wildguard_detector.py
interface.launch(
    share=True,
    server_name="0.0.0.0",
    server_port=8000
)
```

### Option 3: Google Cloud Run
```bash
# Create app.yaml
runtime: python310
env: standard
entrypoint: python wildguard_detector.py

# Deploy
gcloud app deploy
```

## Environment Variables

Set these for production:

```bash
# Gradio config
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=False  # Disable share link in production

# Performance
OMP_NUM_THREADS=4
CUDA_VISIBLE_DEVICES=0  # GPU support if available
```

## Performance Optimization

### For Production
```python
# In wildguard_detector.py
interface.launch(
    share=False,  # Disable sharing
    debug=False,  # Disable debug mode
    server_name="0.0.0.0",
    server_port=8000,
    max_threads=4,
    auth=[("admin", "password")]  # Add auth
)
```

### GPU Acceleration
```bash
# Install GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# YOLOv8 will auto-detect GPU
```

## Monitoring & Logging

### Setup Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wildguard.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

### Health Check Endpoint
```python
@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200
```

## Security Considerations

1. **Authentication**: Add user authentication
2. **Rate Limiting**: Implement request throttling
3. **File Upload**: Validate image files before processing
4. **Model Security**: Use official YOLOv8 models only
5. **Data Privacy**: Don't store uploaded images

## Scaling

### Horizontal Scaling
- Deploy multiple instances behind load balancer
- Use message queue for job distribution
- Cache model in memory

### Vertical Scaling
- Increase server resources (CPU/GPU)
- Optimize model inference
- Use model quantization

## Troubleshooting Deployment

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in server_port parameter |
| GPU not detected | Verify CUDA installation and drivers |
| Slow inference | Enable GPU acceleration or use smaller model |
| Memory issues | Reduce batch size or use model quantization |
| Timeout errors | Increase timeout values in Gradio config |

## Testing Deployed Version

```bash
# Load test
while true; do
  curl -X POST http://localhost:7860/api/predict \
    -H "Content-Type: application/json" \
    -d '{"image": "...base64..."}' 
  sleep 1
done
```

## Rollback Procedure

```bash
# Docker rollback
docker run -p 7860:7860 wildguard:previous
```

## Maintenance

- Monitor logs for errors
- Update dependencies monthly
- Test with new YOLOv8 releases
- Backup model files
- Monitor resource usage
