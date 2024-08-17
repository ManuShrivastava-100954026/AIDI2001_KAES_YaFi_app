from openai import OpenAI
import json

client = OpenAI(api_key="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")


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
