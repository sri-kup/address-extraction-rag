def chunk_text(text, chunk_size=500):
    """
    Splits the input text into chunks of specified size (basic version).
    """
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks