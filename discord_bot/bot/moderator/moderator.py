#IMPORTS:
import requests as req
from openai import OpenAI
import pprint
import sys

client = OpenAI(api_key='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')

print('Ran moderator')

def evaluate(message):
    """
        Reads in message object and passess it into Moderation Model for inference.
    """
    
    print(message)
    
    #Call stringify method of object to send to Moderation Model.
    # message = message.stringify()

    # headers = {"Content-Type": "application/json","Authorization" : "Bearer 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"}

    # data = {"input": "keep yourself safe"} #Sample test message
    
    response = client.moderations.create(input=message)
    
    # r = req.post('https://api.openai.com/v1/moderations', headers=headers, data=data)
    # r = req.post('https://httpbin.org/post', data={'key': 'value'})

    return response.results[0].flagged

# if __name__ == "__main__":
#     message = sys.argv[1:]
#     message = ' '.join(message)
#     evaluate(message)