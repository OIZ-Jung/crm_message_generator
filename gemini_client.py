# gemini_client.py

import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_text(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text

def generate_text_stream(prompt: str):
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        try:
            if chunk.parts:
                yield chunk.text
        except ValueError:
            continue