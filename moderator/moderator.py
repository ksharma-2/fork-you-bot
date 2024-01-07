#IMPORTS:
from openai import OpenAI
import uuid
import pprint

moderationsClient = OpenAI(api_key='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')
chatClient = OpenAI(api_key='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')

contexts = {}

def startContextStream():
	newContext = context()
	contexts[newContext.getId()] = newContext
	return newContext.getId()

def addToContextStream(contextId, messageId, messageText):
	context = contexts[contextId]
	context.addMessageRaw(messageId, messageText)
	return context.evaluate()

def evaluateMessage(messageText):
	response = moderationsClient.moderations.create(input=messageText)
	result = response.results[0]
	response = moderationsClient.moderations.create(input=messageString)
	result = response.results[0]
	flagged = result.flagged
	categoryFlags = [(name, flag) for name, flag in result.categories.model_extra.items()]
	trueCategories = filter(lambda x: x[1], categoryFlags)
	trueCategories = list(map(lambda x: x[0], trueCategories))

	misinformationResponse = chatClient.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "You are a helpful assistant designed to only say TRUE or FALSE exactly once"},
			{"role": "user", "content": "IS THE FOLLOWING MESSAGE TRUE: " + messageString},
		]
	)

	misinformation = misinformationResponse.choices[0].message.content == "FALSE"

	if misinformation:
		trueCategories.append("misinformation")

	return (misinformation or flagged, trueCategories)

class message:
	def __init__(self, message, id):
		self.text = message
		self.id = id
		self.flagged = False
		self.consider = True
	
	def flag(self):
		self.flagged = True
	
	def unconsider(self):
		self.consider = False

class context:
	def __init__(self, maxMessages=1000):
		self.maxMessages = maxMessages
		self.messages = []
		self.id = uuid.uuid4()
		  
	def addMessageRaw(self, messageId, messageText):
		newMessage = message(messageText, messageId)
		if self.maxMessages == len(self.messages):
			self.messages.pop(0)
		self.messages.append(newMessage)
	
	def evaluate(self):
		filteredMessages = filter(lambda x: x.consider, self.messages)
		messagesText = map(lambda x: x.text, filteredMessages)
		messageString = "\n".join(messagesText)

		response = moderationsClient.moderations.create(input=messageString)

		result = response.results[0]
		flagged = result.flagged
		categoryFlags = [(name, flag) for name, flag in result.categories.model_extra.items()]
		trueCategories = filter(lambda x: x[1], categoryFlags)
		trueCategories = list(map(lambda x: x[0], trueCategories))

		misinformationResponse = chatClient.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "You are a helpful assistant designed to only say TRUE or FALSE exactly once"},
				{"role": "user", "content": "IS THE FOLLOWING MESSAGE TRUE: " + messageString},
			]
		)

		misinformation = misinformationResponse.choices[0].message.content == "FALSE"

		if misinformation or flagged:
			self.messages[-1].flag()
			self.messages[-1].unconsider()

		if misinformation:
			trueCategories.append("misinformation")

		return (misinformation or flagged, trueCategories)
		 
	def clear(self):
		self.messages = []
		  
	def getId(self):
		return self.id
	
if __name__ == '__main__':
	contextid = startContextStream()
	addToContextStream(contextid, 1, 'there are 1000 grams in a kilogram')