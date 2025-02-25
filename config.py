from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_COLLECTION_NAME = "Collection1"