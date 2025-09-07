#!/usr/bin/env python3
"""
Setup script for Colab tutorial - Knowledge Enrichment of the Khafre Pipeline
This script downloads the tutorial data and sets up the environment.
"""

import os
import zipfile
import requests
from pathlib import Path

def setup_tutorial_data():
    """Download and setup tutorial data for Colab."""
    
    # GitHub repository URL
    REPO_URL = "https://github.com/StenDoipanni/demos-tutorials/archive/main.zip"
    
    print("Setting up tutorial data...")
    
    # Create data directory
    data_dir = Path("/content/tutorial-fois-2025")
    data_dir.mkdir(exist_ok=True)
    
    try:
        # Method 1: Download from GitHub
        print("Downloading data from GitHub...")
        response = requests.get(REPO_URL)
        response.raise_for_status()
        
        # Save zip file
        zip_path = "/content/tutorial_data.zip"
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        # Extract zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("/content/")
        
        # Move extracted files to the right location
        extracted_dir = "/content/demos-tutorials-main"
        tutorial_dir = "/content/demos-tutorials-main/tutorial-fois-2025"
        if os.path.exists(tutorial_dir):
            os.system(f"mv {tutorial_dir}/* {data_dir}/")
            os.system(f"rm -rf {extracted_dir}")
        elif os.path.exists(extracted_dir):
            os.system(f"mv {extracted_dir}/* {data_dir}/")
            os.system(f"rm -rf {extracted_dir}")
        
        # Clean up
        os.remove(zip_path)
        
        print("✅ Data downloaded and extracted successfully!")
        
    except Exception as e:
        print(f"❌ Error downloading from GitHub: {e}")
        print("Falling back to creating sample data...")
        create_sample_data(data_dir)
    
    # Verify setup
    verify_setup(data_dir)

def create_sample_data(data_dir):
    """Create sample data if download fails."""
    print("Creating sample data...")
    
    # Create event_frames directory
    event_frames_dir = data_dir / "event_frames"
    event_frames_dir.mkdir(exist_ok=True)
    
    # Create sample TTL files
    sample_ttl_content = """@prefix log: <file://./log.owl#> .

log:contact1 a log:Contact .
log:support1 a log:Support .
log:cutting1 a log:Cutting .
log:person1 a log:Person .
log:knife1 a log:Knife .
"""
    
    for i in range(1, 4):
        ttl_file = event_frames_dir / f"sample{i}.ttl"
        with open(ttl_file, 'w') as f:
            f.write(sample_ttl_content)
    
    # Create sample images
    try:
        from PIL import Image, ImageDraw
        
        for i in range(1, 4):
            img = Image.new('RGB', (400, 300), color='lightblue')
            draw = ImageDraw.Draw(img)
            text = f'Sample {i} Image\\nCorresponding to sample{i}.ttl'
            draw.text((50, 150), text, fill='black')
            img.save(event_frames_dir / f"sample{i}.png")
        
        print("✅ Sample data created successfully!")
        
    except ImportError:
        print("⚠️  PIL not available, skipping image creation")

def verify_setup(data_dir):
    """Verify that the setup is correct."""
    print("\\nVerifying setup...")
    
    # Check if event_frames directory exists
    event_frames_dir = data_dir / "event_frames"
    if not event_frames_dir.exists():
        print("❌ event_frames directory not found!")
        return False
    
    # Count TTL and image files
    ttl_files = list(event_frames_dir.glob("*.ttl"))
    image_files = list(event_frames_dir.glob("*.png")) + list(event_frames_dir.glob("*.jpg"))
    
    print(f"Found {len(ttl_files)} TTL files")
    print(f"Found {len(image_files)} image files")
    
    if len(ttl_files) == 0:
        print("❌ No TTL files found!")
        return False
    
    if len(image_files) == 0:
        print("⚠️  No image files found - tutorial will work but without image enrichment")
    
    print("✅ Setup verification complete!")
    return True

if __name__ == "__main__":
    print("🚀 Setting up Knowledge Enrichment Tutorial...")
    setup_tutorial_data()
    print("\\n🎉 Setup complete! You can now run the tutorial cells.")
