import fitz
import sys
import os

from PIL import Image, ImageDraw, ImageFont

def get_label_font(font_size=22):
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
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)
        font = get_label_font(font_size)
        bbox = draw.textbbox((0, 0), label_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        box_x0 = 0
        box_y0 = 0
        box_x1 = box_x0 + text_w + padding_x * 2
        box_y1 = box_y0 + text_h + padding_y * 2
        
        draw.rectangle([box_x0, box_y0, box_x1, box_y1], fill=(0, 0, 0))
        text_x = box_x0 + padding_x - bbox[0]
        text_y = box_y0 + padding_y - bbox[1]
        draw.text((text_x, text_y), label_text, fill=(255, 0, 0), font=font)
        img.save(image_path, "PNG")

def pdf_to_images(pdf_path, output_dir, dpi=100, label=False, font_size=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Opening {pdf_path}...")
    doc = fitz.open(pdf_path)
    folder_name = os.path.basename(os.path.normpath(output_dir))
    
    if font_size is None:
        # Scale font size proportionally with DPI (approx 12px at 100 DPI, 15px at 150 DPI)
        font_size = max(11, int(dpi * 0.11))
    
    # Calculate matrix for the desired DPI (default PDF is 72 DPI)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    
    print(f"Exporting {len(doc)} pages as PNGs at {dpi} DPI (font size: {font_size})...")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=mat)
        
        # Format filename like page_001.png
        filename = f"page_{page_num + 1:03d}.png"
        output_file = os.path.join(output_dir, filename)
        pix.save(output_file)
        
        if label:
            label_text = f"{folder_name}/{filename}"
            add_label_to_image(output_file, label_text, font_size=font_size)
        
        if (page_num + 1) % 10 == 0:
            print(f"Processed {page_num + 1}/{len(doc)} pages...")
            
    print(f"Successfully exported all pages to {output_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert PDF to PNG images")
    parser.add_argument("input_pdf", help="Path to the PDF file")
    parser.add_argument("--out", default="pages_png", help="Output directory")
    parser.add_argument("--dpi", type=int, default=100, help="DPI for output images (default: 100)")
    parser.add_argument("--label", action="store_true", help="Add top-left black box with red filename label")
    parser.add_argument("--font-size", type=int, default=None, help="Font size for the label (default: auto-scaled)")
    
    args = parser.parse_args()
    pdf_to_images(args.input_pdf, args.out, args.dpi, label=args.label, font_size=args.font_size)



