import sys
import os

try:
    import pypdf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pypdf', '--quiet', '--disable-pip-version-check'])
    import pypdf

pdf_path = r"C:\Users\Daniel Palma\Downloads\pdf agendar brasil\PPC_CDA_compressed.pdf"
try:
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for idx, page in enumerate(reader.pages):
        text += f"\n--- Pagina {idx+1} ---\n"
        page_text = page.extract_text()
        if page_text:
           text += page_text
    
    out_path = r"C:\Users\Daniel Palma\Downloads\pdf agendar brasil\PPC_CDA_text.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extraction successful: {len(text)} characters saved to {out_path}")
except Exception as e:
    print(f"Error: {e}")
