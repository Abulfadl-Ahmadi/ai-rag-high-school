I will send you images one by one. Please follow these exact rules for processing each image:

1. **Page Number Source**: 
   - Each image has a black box in the top-left corner with red text showing the filename, for example: "dini-12_images/page_009.png".
   - Extract the page number from that filename (e.g., "009" → Page 9). Do NOT use sequential numbering based on the order I send them.

2. **Page Separator**:
   - Start each page output with:
     ================== PAGE <number> ==================
   - Replace <number> with the extracted page number from the filename (e.g., PAGE 9).

3. **Text Extraction**:
   - Extract ALL text exactly as written in the image (Persian and Arabic), including typos, punctuation, and spacing. Preserve paragraph breaks and headings.

4. **Image/Figure Embedding with Universal Description**:
   - For EVERY image, figure, graph, table, or visual element present in the page, embed it using the following format:
     [fig:<filename>|<coordinates>] (توضیح: [description])
   - Where:
     - <filename> = the exact filename from the black box (e.g., page_009.png).
     - <coordinates> = (x1,y1),(x2,y2), where:
       - (x1,y1) = top-left corner of the figure as a percentage of the whole page (0 to 100).
       - (x2,y2) = bottom-right corner of the figure as a percentage of the whole page (0 to 100).
     - Example: [fig:page_009.png|(20,30),(80,90)]
   - **RULE FOR DESCRIPTIONS (MANDATORY FOR ALL FIGURES):**
     - You MUST provide a detailed, descriptive text in Persian (Farsi) inside parentheses immediately after the [fig] tag.
     - Write the description as if you are explaining the visual element to a blind person. Describe colors, shapes, position, subject matter, actions, and any visual details.
     - Even if the image is a simple icon, a decorative border, or a full-page graphic, you MUST still describe it (e.g., "A decorative green patterned border", "A small QR code icon", "A full-page colorful abstract explosion of light", etc.).
   - Example of full output: 
     `[fig:page_009.png|(0,0),(100,100)] (توضیح: یک عکس سیاه‌و‌سفید از سید روح‌الله خمینی با لباس روحانیت و عمامه سیاه در حالی که به سمت راست نگاه می‌کند. در سمت راست تصویر، یک باکس سبز رنگ حاوی متن وجود دارد.)`

5. **Special Cases**:
   - If a page has NO figures/images: output only the extracted text.
   - If a page has ONLY an image (no text): output the [fig] tag with coordinates and the mandatory description, and nothing else.

6. **Language**:
   - Output the main text in the original language of the image (Persian/Arabic) with exact script and spelling.
   - The descriptive text (توضیح) for the image MUST be written in Persian (Farsi), regardless of the main text language.

7. **Important**:
   - Always read the filename from the black box in the top-left corner.
   - Always use the page number from that filename, NOT the order of sending.

Process each image I send according to these rules and give me the complete output.