from docling.document_converter import DocumentConverter
from nltk_setup import setup_nltk
from pdf_processing import read_pdf, create_markdown, extract_keywords
import locationtagger
import tiktoken
from pathlib import Path
from chunking import *
from vector_store_chroma import *
from groq_client import *



if __name__ == "__main__":
    chunk_id_counter = 0
    GPE_LOC_list = []
    setup_nltk()
    # returns all file paths that has .pdf as extension in the specified directory
    pdf_search = Path("Files/").glob("*.pdf")
    # convert the glob generator output to list
    pdf_files = [str(file.absolute()) for file in pdf_search]
    print(pdf_files)

    # Tokenizer initialization
    encoding = tiktoken.get_encoding("cl100k_base")  # Use appropriate encoding


    converter = DocumentConverter()
    all_docs_dict = {}
    for source in pdf_files:
        all_docs_dict[source] = {}
        doc = read_pdf(source, converter)

        pages_md = create_markdown(doc)
        full_pages_md = ' '.join(pages_md)
        all_docs_dict[source]['pages_md'] = pages_md

        all_docs_dict[source]['place_entity'] = locationtagger.find_locations(text = full_pages_md)

        all_docs_dict[source]['keywords'] = extract_keywords(full_pages_md)

        chromadb_client, collection, vector_store = vector_store_creation()

        # chunk_id_counter = 0
        GPE_LOC_list = []
        all_docs_dict[source]['chunks'], chunk_id_counter = chunk_by_headings_and_threshold(GPE_LOC_list, chunk_id_counter, encoding, source, full_pages_md, pages_md)
        all_docs_dict[source]['GPE_LOC'] = GPE_LOC_list

        print(f"Storing chunks for Doc - {source}")
        store_chunks_in_chromadb(collection, all_docs_dict[source])
        print(f"Completed storing chunks for Doc - {source} -- Collection count - {collection.count()}")

        final_res = query_chromadb(vector_store, 
            f"address location house street locality city state pin zip address line {all_docs_dict[source]['place_entity'].cities} {all_docs_dict[source]['keywords']}",
            where_condition = {'doc_name':source}
            )
        
        prompt = prepare_prompt(final_res)
        completion = extract_addresses(prompt)
        print('---------------------------------------------------')
        print(f'Addresses found in {source} :')
        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end="")
        print('\n---------------------------------------------------')