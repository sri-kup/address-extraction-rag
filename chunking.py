import re
from pdf_processing import clean
from nltk_setup import nlp


def generate_chunk_id(chunk_id_counter):
    chunk_id = str(chunk_id_counter)
    chunk_id_counter += 1
    return chunk_id, chunk_id_counter

# Function to extract metadata
def extract_metadata(GPE_LOC_list, source, chunk, pages, chunk_id):
    chunk = clean(chunk)
    doc = nlp(chunk)

    metadata = {"doc_name":source, "pages": str(pages), "chunk_id": chunk_id, "location": False}
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
          if ent.text.strip().lower() not in GPE_LOC_list:
            GPE_LOC_list.append(ent.text.strip().lower())
          metadata["location"] = True
          break

    return metadata

def num_tokens_from_string(encoding, string: str) -> int:
    """Returns the number of tokens in a text string."""
    return len(encoding.encode(string))

def split_text_by_tokens(encoding, text, threshold, overlap=0):
    """
    Split text into chunks based on token count.
    """
    tokens = encoding.encode(text)
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + threshold
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        start = end - overlap  # Apply overlap if specified

    return chunks

def chunk_by_headings_and_threshold(GPE_LOC_list, chunk_id_counter, encoding, source, text, pages_markdown, threshold=300):
    pattern = r"(#+\s+.*)"
    headers = re.findall(pattern, text)  # Extract headers from text

    chunks = []  # List to store chunks
    last_index = 0  # Keeps track of the end index of the last processed header

    current_chunk = ""  # Holds the current chunk's content
    current_pages = []  # Pages where the current chunk appears
    for i, header in enumerate(headers):  # Iterate over each header
        start_index = text.find(header, last_index)  # Header's start
        end_index = text.find(headers[i + 1], start_index) if i + 1 < len(headers) else len(text)  # Next header or EOF

        chunk = text[start_index:end_index].strip()

        chunk_pages = []
        for page_no, page_markdown in enumerate(pages_markdown):
            if chunk in page_markdown:
                chunk_pages.append(page_no+1)
                break

        if num_tokens_from_string(encoding, chunk) > threshold:
            if current_chunk:
                chunk_id, chunk_id_counter = generate_chunk_id(chunk_id_counter)
                chunks.append({
                    'chunk_text': current_chunk.strip(),
                    'chunk_metadata': extract_metadata(GPE_LOC_list, source, current_chunk, current_pages, chunk_id)
                })
                current_chunk = ""
                current_pages = []

            # Token-based splitting
            for split in split_text_by_tokens(encoding, chunk, threshold, overlap=threshold // 10):
                chunk_id, chunk_id_counter = generate_chunk_id(chunk_id_counter)
                chunks.append({
                    'chunk_text': split.strip(),
                    'chunk_metadata': extract_metadata(GPE_LOC_list, source, split, current_pages, chunk_id)
                })
        else:
            if num_tokens_from_string(encoding, current_chunk) + num_tokens_from_string(encoding, chunk) > threshold:
                chunk_id, chunk_id_counter = generate_chunk_id(chunk_id_counter)
                chunks.append({
                    'chunk_text': current_chunk.strip(),
                    'chunk_metadata': extract_metadata(GPE_LOC_list, source, current_chunk, current_pages, chunk_id)
                })

                current_chunk = chunk
                current_pages = chunk_pages
            else:
                # Merge if under threshold
                current_chunk += "\n" + chunk
                current_pages.extend(chunk_pages)

        last_index = end_index

    # Final chunk after processing
    if current_chunk:
        chunk_id, chunk_id_counter = generate_chunk_id(chunk_id_counter)
        chunks.append({
            'chunk_text': current_chunk.strip(),
            'chunk_metadata': extract_metadata(GPE_LOC_list, source, current_chunk, current_pages, chunk_id)
        })

    return chunks, chunk_id_counter