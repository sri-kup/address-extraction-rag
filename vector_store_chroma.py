import chromadb
import uuid

def get_chroma_client(persist_directory="chroma_db"):
    """
    Initializes and returns a Chroma client.
    """
    client = chromadb.PersistentClient(path=persist_directory)
    return client

def create_collection(client, collection_name="default_collection"):
    """
    Creates or retrieves a collection in Chroma.
    """
    return client.get_or_create_collection(name=collection_name)

def upsert_chunks(collection, chunks):
    """
    Inserts or updates chunks into the Chroma collection.
    """
    ids = [str(uuid.uuid4()) for _ in chunks]
    collection.upsert(
        ids=ids,
        documents=chunks
    )
    print(f"Inserted {len(chunks)} chunks into vector store.")