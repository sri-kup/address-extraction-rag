import PyPDF2

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using PyPDF2 (basic version).
    """
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    
    return text
