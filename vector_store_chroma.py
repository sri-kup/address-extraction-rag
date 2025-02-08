import chromadb

def get_chroma_client(persist_directory="chroma_db"):
    """
    Initializes and returns a Chroma client (basic draft version).
    """
    client = chromadb.PersistentClient(path=persist_directory)
    return client

def create_collection(client, collection_name="default_collection"):
    """
    Creates or retrieves a collection in Chroma (basic draft version).
    """
    return client.get_or_create_collection(name=collection_name)