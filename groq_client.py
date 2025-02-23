from groq import Groq
from config import GROQ_API_KEY
import ast

# Initialize the Groq client
Groq_client = Groq()

# Function to prepare the prompt for the LLM to extract addresses
def prepare_prompt(chunks):
    prompt = "Extract a list of all physical addresses mentioned in the following text:\n\n"
    # docs = '\n'.join([item for sublist in final_res['documents'] for item in sublist])
    docs = '\n'.join([f"(Content - {doc.page_content}, Page No. - {ast.literal_eval(doc.metadata['pages'])})" for doc in chunks])
    prompt += docs

    return prompt


def extract_addresses(prompt):
    # Create a Groq completion request to extract the list of addresses
    completion = Groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": """
You are an assistant that extracts physical addresses from provided document chunks. 
You will receive data in the following format: 
(Content - <content>, Page No. - <page_numbers>)

Your task:
1. Analyze each (Content - Page No.) pair **independently**.
2. Extract only **complete physical addresses** from the content if present.
3. If an address is found, **associate it only with the exact page number(s)** given in the pair.
4. **Do not infer or guess page numbers** from other pairs or sections.
5. If no address is present in a particular content chunk, **ignore that chunk** without referencing its page number.
6. Present the results in the following format:

- <Extracted Address 1> — Found on page(s): <page_number>
- <Extracted Address 2> — Found on page(s): <page_number>
- ...

⚡️ **Important:**  
- Only list addresses **you are certain** about.  
- **Do not merge page numbers** across different content chunks.  
- If no addresses are found in the entire content, respond with: **"No addresses found."**  
"""
        },
        {
             "role": "user", "content": prompt
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

    return completion
