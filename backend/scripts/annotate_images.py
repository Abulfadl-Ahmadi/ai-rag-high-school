import os
import glob
import argparse
from PIL import Image, ImageDraw, ImageFont

def get_font(font_size=22):
    font_candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/consola.ttf",
        "arial.ttf",
    ]
    for font_path in font_candidates:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, font_size)
            except Exception:
                pass
    try:
        return ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        return ImageFont.load_default()

def add_label_to_image(image_path, label_text, font_size=22, padding_x=6, padding_y=4):
    """
    Opens an image, draws a small black box in the top-left corner,
    and writes the label_text in red inside the box.
    """
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)
        font = get_font(font_size)
        
        # Calculate text bounding box
        bbox = draw.textbbox((0, 0), label_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        box_x0 = 0
        box_y0 = 0
        box_x1 = box_x0 + text_w + padding_x * 2
        box_y1 = box_y0 + text_h + padding_y * 2
        
        # Draw black rectangle
        draw.rectangle([box_x0, box_y0, box_x1, box_y1], fill=(0, 0, 0))
        
        # Draw red text
        text_x = box_x0 + padding_x - bbox[0]
        text_y = box_y0 + padding_y - bbox[1]
        draw.text((text_x, text_y), label_text, fill=(255, 0, 0), font=font)
        
        img.save(image_path, "PNG")

def process_directory(directory_path, font_size=22):
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        return

    folder_name = os.path.basename(os.path.normpath(directory_path))
    image_extensions = ("*.png", "*.jpg", "*.jpeg", "*.webp")
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(directory_path, ext)))
    
    # Sort files naturally
    image_files = sorted(image_files)
    
    total = len(image_files)
    print(f"Found {total} images in {directory_path} to label...")
    
    for idx, img_path in enumerate(image_files, 1):
        filename = os.path.basename(img_path)
        label_text = f"{folder_name}/{filename}"
        add_label_to_image(img_path, label_text, font_size=font_size)
        
        if idx % 10 == 0 or idx == total:
            print(f"Labeled {idx}/{total} images ({filename})...")
            
    print("Done! All images have been updated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add top-left black box with red filename label on images")
    parser.add_argument("dir", nargs="?", default=r"f:\ai_rag_high_school\dataset\textbooks\dini-12_images", help="Target directory containing images")
    parser.add_argument("--font-size", type=int, default=22, help="Font size for the label (default: 22)")
    
    args = parser.parse_args()
    process_directory(args.dir, font_size=args.font_size)
