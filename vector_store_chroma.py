import chromadb
import uuid
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.utils.embedding_functions import create_langchain_embedding

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

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
    ef = create_langchain_embedding(embeddings)
    return client.get_or_create_collection(name=collection_name, embedding_function=ef)

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