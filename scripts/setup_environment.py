"""
Setup script to install dependencies and prepare WildGuard environment
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    print("Installing WildGuard dependencies...\n")
    
    packages = [
        ("ultralytics", "8.0.228"),
        ("gradio", "4.41.1"),
        ("opencv-python-headless", None),
        ("pillow", None),
        ("numpy", None),
    ]
    
    for package, version in packages:
        if version:
            cmd = f"pip install -q {package}=={version}"
        else:
            cmd = f"pip install -q {package}"
        
        print(f"Installing {package}...", end=" ")
        try:
            subprocess.check_call(cmd.split())
            print("✓")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
            return False
    
    return True


def create_directories():
    """Create necessary directories"""
    print("\nCreating project directories...\n")
    
    dirs = ['test_images', 'outputs', 'models', 'logs']
    
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✓ Created: {dir_name}/")
    
    return True


def verify_installation():
    """Verify all packages installed correctly"""
    print("\nVerifying installation...\n")
    
    modules = [
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
        ('ultralytics', 'YOLOv8'),
        ('gradio', 'Gradio'),
    ]
    
    all_good = True
    for module, name in modules:
        try:
            __import__(module)
            print(f"✓ {name} installed correctly")
        except ImportError:
            print(f"✗ {name} NOT installed")
            all_good = False
    
    return all_good


def main():
    """Main setup routine"""
    print("="*60)
    print("WILDGUARD ENVIRONMENT SETUP")
    print("="*60 + "\n")
    
    if not install_dependencies():
        print("\n✗ Dependency installation failed")
        return False
    
    if not create_directories():
        print("\n✗ Directory creation failed")
        return False
    
    if not verify_installation():
        print("\n✗ Installation verification failed")
        return False
    
    print("\n" + "="*60)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run: python scripts/generate_test_data.py")
    print("2. Run: python scripts/test_wildguard.py")
    print("3. Run: python wildguard_detector.py")
    print()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
