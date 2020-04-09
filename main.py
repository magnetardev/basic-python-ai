from ai import AI
from handlers import handlers
import json

# Load data
f = open("data.json")
data = json.load(f)
f.close()

# Init AI
ai = AI(data=data, handlers=handlers)
print("AI loaded. Type \"quit\" to exit.")

# Run input/response loop
while(True):
	query = input("[You]: ")
	if query.lower() == "quit": break
	res = ai.query(query)
	print(f"[Bot]: {res}")
