#!/bin/bash

# WildGuard Complete Demo Script

echo "╔════════════════════════════════════════════════════╗"
echo "║  WILDGUARD - Complete System Demo                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Step 1: Setup
echo "Step 1: Setting up environment..."
python scripts/setup_environment.py
if [ $? -ne 0 ]; then
    echo "Setup failed!"
    exit 1
fi
echo ""

# Step 2: Generate test data
echo "Step 2: Generating test data..."
python scripts/generate_test_data.py
if [ $? -ne 0 ]; then
    echo "Test data generation failed!"
    exit 1
fi
echo ""

# Step 3: Run tests
echo "Step 3: Running test suite..."
python scripts/test_wildguard.py
if [ $? -ne 0 ]; then
    echo "Tests failed!"
    exit 1
fi
echo ""

# Step 4: Launch interface
echo "Step 4: Launching WildGuard web interface..."
echo "Access at: http://localhost:7860"
echo ""
python wildguard_detector.py
