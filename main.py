from pdf_processing import extract_text_from_pdf
from chunking import chunk_text
from vector_store_chroma import get_chroma_client, create_collection, upsert_chunks
from groq_client import ask_groq
import os

def process_pdf(file_path):
    """
    Process the PDF: extract text, chunk, store chunks, and query Groq.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    print("Extracting text from PDF...")
    text = extract_text_from_pdf(file_path)

    if not text:
        print("No text extracted from PDF.")
        return

    print("Chunking text...")
    chunks = chunk_text(text)

    print("Initializing vector store...")
    client = get_chroma_client()
    collection = create_collection(client)

    print("Storing chunks into vector store...")
    upsert_chunks(collection, chunks)

    print("Querying Groq for first 3 chunks...")
    for chunk in chunks[:3]:
        response = ask_groq(chunk)
        print("Groq Response:", response)

if __name__ == "__main__":
    sample_pdf = "sample.pdf"  # Placeholder PDF path
    process_pdf(sample_pdf)