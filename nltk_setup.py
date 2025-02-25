import nltk
import spacy
nlp = spacy.load("en_core_web_sm")

def setup_nltk():
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')
    nltk.download('maxent_ne_chunker_tab')
    nltk.downloader.download('maxent_ne_chunker')
    nltk.downloader.download('words')
    nltk.downloader.download('treebank')
    nltk.downloader.download('maxent_treebank_pos_tagger')
    nltk.downloader.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')

if __name__ == "__main__":
    setup_nltk()