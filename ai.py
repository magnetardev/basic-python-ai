from statistics import stdev
from math import exp

def memoize(func):
	mem = {}
	def memoizer(*args, **kwargs):
		key = str(args) + str(kwargs)
		if key not in mem:
			mem[key] = func(*args, **kwargs)
		return mem[key]
	return memoizer

class AI:
	def __init__(self, data = [], handlers = dict()):
		self.data = data
		self.handlers = handlers

	# Levenshtein Distance
	# The distance between two strings
	# 0 means the strings are exactly the same.
	# i.e. cat and chat have a lev. dist. of 1, as it is one character off.
	@memoize
	def levDist(self, s, t):
		if s == "":
			return len(t)
		if t == "":
			return len(s)
		if s[-1] == t[-1]:
			cost = 0
		else:
			cost = 1
		
		res = min([self.levDist(s[:-1], t)+1,
				self.levDist(s, t[:-1])+1, 
				self.levDist(s[:-1], t[:-1]) + cost])

		return res

	# Score
	# How accurate the prediction is, based off of statistics from the lev. distances
	# On a scale of 0 to 1 (0 is 100% accurate, 1 is 0% accurate).
	def score(self, dataset):
		# count_dist = len(dataset) 	# How many entries are in the data
		# sum_dist = sum(dataset) 	# More accurate, the lower this will be.
		min_dist = min(dataset) 	# More accurate, the lower this wil be.
		# max_dist = max(dataset) 	# More accurate, the lower this will be.
		stdev_dist = stdev(dataset) # The more accurate, the higher this will be.
		# avg_dist = mean(dataset) 	# 
		if stdev_dist == 0:
			return 1
		else:
			scale = 0.1
			return 1 - exp(-(scale*min_dist))

	# Query
	# Input text and get the AI's response back.
	def query(self, message):
		punctuation = [',', '.', '\'', '"', '!', '?']
		
		# Clean
		query = message.lower().strip()
		for x in punctuation:
			query = query.replace(x, "")
		
		# Get intent
		intent = self.classify(query)

		# Get & Return Response
		if intent in self.handlers:
			response = self.handlers[intent](message)
			return response
		else:
			return "I can't respond to that yet."


	# Classify
	# Take our data, find the most accurate intent, and return that label.
	def classify(self, query, req_score=0.15):
		stats = []

		# Generate stats
		for intent in self.data:
			# Takes one array, turns it into another
			dataset = list(map(lambda x: self.levDist(query, x), intent['data']))
			res = {
				"intent": intent["intent"], # The intent for this set of stats
				"score": self.score(dataset)
			}
			stats.append(res)
		
		scores = list(map(lambda x: x['score'], stats))
		min_score = min(scores)
		min_score_index = scores.index(min_score)
		if min_score <= req_score:
			most_accurate = stats[min_score_index]
			# Return predicted intent
			return most_accurate['intent']
		else:
			return 'unknown'