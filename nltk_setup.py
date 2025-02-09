import nltk

def download_nltk_dependencies():
    """
    Downloads required NLTK packages (basic version).
    """
    nltk.download('punkt')

if __name__ == "__main__":
    download_nltk_dependencies()