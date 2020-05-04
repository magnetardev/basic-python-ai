from operator import itemgetter
import nltk
from geotext import GeoText
from string import punctuation
from random import choice
from os import listdir
import json

nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)

from nltk.corpus import stopwords

def get_nltk_chunk(message, label):
	matches = []
	stop = stopwords.words('english')

	# Get sentences
	document = ' '.join([i for i in message.split() if i not in stop])
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]

	# Get matches
	for tagged_sentence in sentences:
		for chunk in nltk.ne_chunk(tagged_sentence):
			if type(chunk) == nltk.tree.Tree:
				if chunk.label() == label:
					matches.append(' '.join([c[0] for c in chunk]))
		else:
			return matches

def names(message):
	names = []
	stop = stopwords.words('english')

	# Get sentences
	document = ' '.join([i for i in message.split() if i not in stop])
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]

	# Get names
	for tagged_sentence in sentences:
		for chunk in nltk.ne_chunk(tagged_sentence):
			if type(chunk) == nltk.tree.Tree:
				if chunk.label() == 'PERSON':
					names.append(' '.join([c[0] for c in chunk]))
		else:
			return names
	

def organization(message):
	organization = []
	stop = stopwords.words('english')

	# Get sentences
	document = ' '.join([i for i in message.split() if i not in stop])
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]

	# Get organizations
	for tagged_sentence in sentences:
		for chunk in nltk.ne_chunk(tagged_sentence):
			if type(chunk) == nltk.tree.Tree:
				if chunk.label() == 'ORGANIZATION':
					organization.append(' '.join([c[0] for c in chunk]))
		else:
			return organization

# Creates a decorator with the ability to store data in memory
def memory(func):
	mem = {}
	def memorize(*args, **kwargs):
		key = str(args) + str(kwargs)
		if key not in mem:
			mem[key] = func(*args, **kwargs)
		return mem[key]
	return memorize

class Chatbot:
	# Properties
	intents = []
	datasets = []
	handlers = {}
	variables = dict(
		names=lambda msg: get_nltk_chunk(msg, "PERSON"), 
		organizations=lambda msg: get_nltk_chunk(msg, "ORGANIZATION"), 
		cities=lambda msg: GeoText(msg).cities,
		countries=lambda msg: GeoText(msg).countries,
		nationalities=lambda msg: GeoText(msg).nationalities
	)

	# Init Method
	def __init__(self, intents_dir = './intents'):
		# Get files in the intents directory
		intents_files = listdir(intents_dir)

		# Loop through each of the files in the directory
		for filename in intents_files:
			# Only work with it if it's a json file
			if filename.split('.').pop() == 'json':
				# Open the file and parse the JSON file
				f = open(f"{intents_dir}/{filename}".replace('//', '/'))
				intent = json.load(f)

				# Go through each intent and split the data.
				split_data = list(map(lambda data: data.split(' '), intent['data']))

				# Make it so that data is stored like [...] not [[...], [...]]
				flat_data = [item for sublist in split_data for item in sublist]

				# Create a dictionary of for each intent with the words that show up in the data
				data = dict(intent=intent['name'], words=list(set(flat_data)))

				# Store our intents & data
				self.datasets.append(data)
				self.intents.append(intent)
				
				# Close the file
				f.close()

	# Classify Method
	# Takes a string, and tries to find the best result.
	def classify(self, message, min_score=0.5):
		# Clean & break the message into a list of words

		scores = dict()
		for data in self.datasets:
			# Get all the word matches in the string
			# If a word is in the dataset, it'll have a value of 1
			# If a word isn't in the dataset, it'll have a value of 0
			variables = self.get_variables(message, data['intent'])
			flat_values = [item for sublist in variables.values() for item in sublist]
			msg = message
			for string in flat_values:
				msg = msg.replace(string, '')
			features = msg.translate(str.maketrans('', '', punctuation)).lower().split(' ')

			non_variable_words = list(filter(lambda word: word not in flat_values, features))
			# print(non_variable_words)
			matches = list(map(lambda feature: 1 if feature in data['words'] else 0, non_variable_words))

			# Convert the matches to a percent
			percent = sum(matches) / len(matches)

			# Add this intent to our score dictionary
			scores[data['intent']] = percent
		
		# Get the intent with the highest percent
		max_intent = max(scores, key=scores.get)
		variables = self.get_variables(message, max_intent)

		# If the max intent doesn't meet the minimum score 
		# threshold (defaults to .5), we will fallback to 
		# the 'unknown' intent. If it does, return the intent.
		return (max_intent if scores[max_intent] >= min_score else 'unknown', variables)

	# Query Method
	# Takes a message & gets a response from the detected intent.
	def query(self, message, min_score=0.5):
		# Get the intent based of of the message
		classification, variables = self.classify(message, min_score)

		# Filter the intents for the one with the classified  name
		intents = list(filter(lambda intents: intents['name'] == classification, self.intents))

		# If the intents array is greater than one, return a random response
		# If not, then return a default response.
		if len(intents) > 0:
			intent = intents[0]
			handler = self.handlers.get(intent['name'])
			response = choice(intent['responses'])
			if len(intent['variables']) > 0:
				for name in intent['variables']:
					response = response.replace(f"$[{name}]", '{}').format(*variables.get(name, []))
			return handler(response, variables) if handler else response
		else:
			return "I don't know how to respond..."

	# Get variables
	@memory
	def get_variables(self, message, intent_name):
		res_vars = dict()
		intents = list(filter(lambda intents: intents['name'] == intent_name, self.intents))
		if len(intents) > 0:
			intent = intents[0]
			for variable in intent['variables']:
				if variable in self.variables:
					res = self.variables[variable](message)
					res_vars[variable] = res
			else: 
				return res_vars

	# Handler
	# This is a decorator for adding a handler to an intent
	def handler(self, f):
		self.handlers.setdefault(f.__name__, f)
	
	# Variable
	# Add a custom variable
	def variable(self, f):
		self.variables.setdefault(f.__name__, f)
