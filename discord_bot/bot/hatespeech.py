import json

from dotenv import load_dotenv
from expertai.nlapi.cloud.client import ExpertAiClient

load_dotenv('.env.local')
detector = 'hate-speech'
language = 'en'
client = ExpertAiClient()


def evaluate(content):
    output = client.detection(body={"document": {"text": content}}, params={
                              'detector': detector, 'language': language})
    total = 0
    for category in output.categories:
        total += int(category.id_)/100
    categories = [category.hierarchy for category in output.categories]
    return total, categories
