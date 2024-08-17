import openai
from openai import OpenAI
import json
import os


with open('config.json') as f:
    config = json.load(f)

api_key = config["OPEN_API_KEY"]
print(config)
client = OpenAI(api_key=api_key)


def get_openai_response(messages, functions=None):
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            functions=functions,
            function_call='auto'
        )
        return response  # Return the entire response object for further handling
    except Exception as e:
        return str(e)
