#IMPORTS:
import requests as req

print('Ran moderator')

def evaluate(message):
    """
        Reads in message object and passess it into Moderation Model for inference.
    """
    
    #Call stringify method of object to send to Moderation Model.
    # message = message.stringify()

    headers = {"Content-Type": "application/json","Authorization" : "Bearer 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"}

    data = {"input": "keep yourself safe"} #Sample test message

    r = req.post('https://api.openai.com/v1/moderations', headers=headers, data=data)
    # r = req.post('https://httpbin.org/post', data={'key': 'value'})

    print(r.json())

if __name__ == "__main__":
    evaluate("test")
