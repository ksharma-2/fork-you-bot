import requests as req
from openai import OpenAI
import pprint
import sys

client = OpenAI(api_key='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')

def translate(message):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to only produce True or False responses."},
        {"role": "user", "content": "Is the following message in English: " + message}
    ]
    )
    
    if response.choices[0].message.content == "True":
        return message
    else:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed only to translate messages into English."},
            {"role": "user", "content": "Translate the following into English: " + message}
        ]
        )
        return response.choices[0].message.content
    
if __name__ == "__main__":
    message = sys.argv[1:]
    message = ' '.join(message)
    print(translate(message))