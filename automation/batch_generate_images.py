#!/usr/bin/env python3
"""
LogiShift Batch Hero Image Generator
Generates missing hero images for existing cluster articles using DALL-E 3.
"""
import os
import sys
import re
from datetime import datetime

# Adjust path to import automation modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from automation.gemini_client import GeminiClient
except ImportError:
    from gemini_client import GeminiClient

def generate_images_for_existing():
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_articles")
    
    if not os.path.exists(output_dir):
        print(f"Directory not found: {output_dir}")
        return

    gemini = GeminiClient()
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Find all generated markdown files for cluster articles
    md_files = [f for f in os.listdir(output_dir) if f.endswith('.md') and date_str in f]
    
    for filename in md_files:
        filepath = os.path.join(output_dir, filename)
        target_key = filename.replace(f"{date_str}_", "").replace(".md", "")
        image_filename = f"{date_str}_{target_key}_hero.png"
        image_path = os.path.join(output_dir, image_filename)
        
        # Skip if image already exists
        if os.path.exists(image_path):
            print(f"⏩ Image already exists for {target_key}, skipping.")
            continue
            
        print(f"\nProcessing: {filename}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract title from YAML or markdown H1
        title_match = re.search(r'title:\s*"?(.*?)"?\n', content)
        if title_match:
            title = title_match.group(1)
        else:
            title = target_key
            
        print(f"Title: {title}")
        
        # Generate image
        try:
            content_summary = content[:1000]
            print("Requesting image prompt from Gemini...")
            image_prompt = gemini.generate_image_prompt(title, content_summary, "Cluster Article")
            
            print(f"Generating image via DALL-E 3: {image_filename}")
            generated_img = gemini.generate_image(image_prompt, image_path, aspect_ratio="16:9")
            
            if generated_img:
                print(f"✅ Success: {image_filename}")
            else:
                print(f"❌ Failed: {image_filename}")
                
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    generate_images_for_existing()
