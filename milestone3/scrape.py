from raw_markdown import markdown
from pydantic import create_model
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import time
from assets_variables import gemini_flash_key, system_prompt, user_prompt


def divide_chunks(text, max_tokens):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1
        if current_length + word_length > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def process_chunks(chunks, system_prompt, user_prompt, model):
    responses = []
    for chunk in chunks:
        prompt = f"{system_prompt} \n {user_prompt} {chunk}"
        response = model.generate_content(prompt, request_options={"timeout": 600})
        json_response = json.loads(response.text)
        responses.extend(json_response["listings"])
    return {"listings": responses}

def pydantic_model(fields):
    field_definitions = {field: (str, ...) for field in fields}
    return create_model("DynamicListingModel", **field_definitions)

def pydantic_container(model):
    return create_model("DynamicListingsContainer", listings=(list[model], ...))

def scrape(fields, url):
    global response
    if fields:
        dynamic_model = pydantic_model(fields)
        dynamic_listing_container = pydantic_container(dynamic_model)
        genai.configure(api_key=gemini_flash_key)

        model = genai.GenerativeModel("gemini-1.5-flash", generation_config={
            "response_schema": dynamic_listing_container,
            "response_mime_type":"application/json"
        })
        raw_data = markdown(url)
        chunks = list(divide_chunks(raw_data, 1600))
        response = process_chunks(chunks, system_prompt, user_prompt, model)
        return response