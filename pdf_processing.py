from rake_nltk import Rake
import re

# Clean the text
def clean(chunk):
    chunk = chunk.replace('\n', ' ')
    chunk = re.sub(r'\s+', ' ', chunk)
    chunk = chunk.strip()
    chunk = chunk.replace('  ', ' ')
    chunk = chunk.replace('#', '')
    chunk = chunk.replace('**', '')
    return chunk

def create_markdown(doc):
  # Get total number of pages
  total_pages = len(doc.pages)

  # Extract markdown for each page
  pages_markdown = [doc.export_to_markdown(page_no=i) for i in range(1,total_pages+1) ]
  return pages_markdown

def read_pdf(source, converter):
  result = converter.convert(source)
  return result.document

def extract_keywords(text):
  # Initialize RAKE
  r = Rake(max_length=4)

  # Extract keywords from the text
  text = clean(text)
  text = text.replace('.', '')
  r.extract_keywords_from_text(text)

  # Get the ranked phrases
  keywords_rake = r.get_ranked_phrases_with_scores()

  unique_entries = []
  seen = set()
  # Iterate through sorted data and collect unique entries
  for score, text in keywords_rake:
      if text not in seen:
          unique_entries.append(text)
          seen.add(text)
      if len(unique_entries) == 10:  # Stop when we have k unique entries
          break
  return unique_entries