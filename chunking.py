import nltk
from config import CHUNK_SIZE

nltk.download('punkt', quiet=True)

def chunk_text(text, chunk_size=CHUNK_SIZE):
    """
    Splits text into chunks based on sentences with a max chunk size.
    """
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks