import spacy
import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.utils.embedding_functions import create_langchain_embedding

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def vector_store_creation():

    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")This is a business requirement. 

    ef = create_langchain_embedding(embeddings)
    collection_name = "Collection1"

    # Initialize Chroma client for persistence (if needed)
    chromadb_client = chromadb.PersistentClient()
    collection = chromadb_client.get_or_create_collection(collection_name, embedding_function=ef)

    # Initialize the Chroma vector store
    vector_store = Chroma(
        client=chromadb_client,
        collection_name=collection_name,
        embedding_function=embeddings,
        # persist_directory="./chroma_langchain_db",  # Optional persistence
    )

    return chromadb_client, collection, vector_store


def store_chunks_in_chromadb(collection, full_doc_dict):
  chunks = full_doc_dict['chunks']
  for chunk in chunks:
      chunk_id = chunk['chunk_metadata']['chunk_id']

      # Add document, embedding, and metadata to Chroma
      collection.add(
          ids=[chunk_id],
          documents=[chunk['chunk_text']],  # Store the chunk content here
          # embeddings=[chunk_embedding],  # Store the embeddings
          metadatas=[chunk['chunk_metadata']]  # Store the metadata
      )

def query_chromadb(vector_store, query_text, where_condition = None):

    results = vector_store.similarity_search_by_vector(
    embedding=embeddings.embed_query(query_text), k=10, filter = where_condition
)
    return results
