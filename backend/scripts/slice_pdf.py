import sys
from pypdf import PdfReader, PdfWriter

def slice_pdf(input_path, output_path, start_page, end_page):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Handle zero-based index
    start = max(0, start_page - 1)
    end = min(len(reader.pages), end_page)
    
    for i in range(start, end):
        writer.add_page(reader.pages[i])
        
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)
    
    print(f"Created slice with pages {start_page} to {end_page} at {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input pdf")
    parser.add_argument("output", help="output pdf")
    parser.add_argument("start", type=int, help="start page (1-based)")
    parser.add_argument("end", type=int, help="end page (inclusive)")
    args = parser.parse_args()
    
    slice_pdf(args.input, args.output, args.start, args.end)
