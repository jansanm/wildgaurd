"""
Demo runner with preset test cases for WildGuard
"""

from pathlib import Path
import sys
import os

def run_demo():
    """Run interactive demo"""
    print("\n" + "="*60)
    print("WILDGUARD DEMO RUNNER")
    print("="*60 + "\n")
    
    demo_steps = [
        {
            "title": "Step 1: Environment Setup",
            "command": "python scripts/setup_environment.py",
            "description": "Install dependencies and create directories"
        },
        {
            "title": "Step 2: Generate Test Data",
            "command": "python scripts/generate_test_data.py",
            "description": "Create synthetic wildlife detection test images"
        },
        {
            "title": "Step 3: Run Test Suite",
            "command": "python scripts/test_wildguard.py",
            "description": "Execute comprehensive system tests"
        },
        {
            "title": "Step 4: Launch Web Interface",
            "command": "python wildguard_detector.py",
            "description": "Start Gradio interface for interactive testing"
        }
    ]
    
    print("Quick Start Guide:\n")
    for i, step in enumerate(demo_steps, 1):
        print(f"{step['title']}")
        print(f"  Command: {step['command']}")
        print(f"  Purpose: {step['description']}\n")
    
    print("="*60)
    print("\nTo run all steps automatically:")
    print("  python scripts/demo_runner.py --auto\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        import subprocess
        for step in demo_steps:
            print(f"\nExecuting: {step['title']}")
            print("-" * 60)
            try:
                subprocess.run(step['command'].split(), check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error executing: {step['command']}")
                break


if __name__ == "__main__":
    run_demo()
