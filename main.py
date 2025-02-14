from pdf_processing import extract_text_from_pdf
from chunking import chunk_text
from vector_store_chroma import get_chroma_client, create_collection
from groq_client import ask_groq

def process_pdf(file_path):
    """
    Process the PDF: extract text, chunk, store, and ask Groq (initial version).
    """
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(file_path)

    print("Chunking text...")
    chunks = chunk_text(text)

    print("Initializing vector store...")
    client = get_chroma_client()
    collection = create_collection(client)

    print("Processing chunks with Groq...")
    for chunk in chunks[:3]:  # Process only first 3 chunks as a sample
        response = ask_groq(chunk)
        print("Groq Response:", response)

if __name__ == "__main__":
    sample_pdf = "sample.pdf"  # Placeholder PDF path
    process_pdf(sample_pdf)