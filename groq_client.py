import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(question, model="mixtral-8x7b-32768"):
    """
    Send a simple question to Groq API and return the response.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content.strip()