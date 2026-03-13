import sys
import os
import pypdf

pdf_path = r"C:\Users\Daniel Palma\Downloads\pdf agendar brasil\PPC_CDA_compressed.pdf"
out_path = r"C:\Users\Daniel Palma\Downloads\pdf agendar brasil\PPC_CDA_text.txt"

print(f"Reading {pdf_path}")
try:
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for idx, page in enumerate(reader.pages):
        text += f"\n--- Pagina {idx+1} ---\n"
        page_text = page.extract_text()
        if page_text:
           text += page_text
        if idx > 0 and idx % 10 == 0:
            print(f"Read {idx} pages...")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extraction successful: {len(text)} characters saved to {out_path}")
except Exception as e:
    print(f"Error: {e}")
