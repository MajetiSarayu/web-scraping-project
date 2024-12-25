import os

# using genai library

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

genai.configure(api_key=os.environ["api-key"])

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Tell me a joke")
print(response.text)


# using langchain

from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    api_key=os.environ["api-key"],
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

messages = [
    (
        "system",
        "You are a helpful assistant that answers a question",
    ),
    ("human", "tell me about python in 100 words"),
]
response = model.invoke(messages)
print(response.content)
