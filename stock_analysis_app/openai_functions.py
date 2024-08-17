import openai
from openai import OpenAI
import json
import os

'''
with open('config.json') as f:
    config = json.load(f)

api_key = config["OPEN_API_KEY"]
print(config)

api_key = os.getenv('OPENAI_API_KEY')

# Ensure the path to the config.json file is correct
config_path = os.path.join(os.path.dirname(__file__), 'config.json')

def load_api_key():
    with open(config_path, 'r') as file:
        config = json.load(file)
        return config.get('OPENAI_API_KEY')

api_key = load_api_key()
'''
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client with the API key
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
