# import os

# from google import genai


# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise RuntimeError(
#         "GEMINI_API_KEY environment variable is not set"
#     )


# client = genai.Client(
#     api_key=GEMINI_API_KEY
# )


# MODEL_NAME = "gemini-3.7-flash"


# def generate_text(prompt: str) -> str:

#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt,
#     )

#     return response.text

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_retries=2,
    google_api_key=GEMINI_API_KEY,
)