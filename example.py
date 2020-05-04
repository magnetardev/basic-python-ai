from chatbot import Chatbot

# Setup the bot with the data from ./intents
bot = Chatbot()

@bot.handler
def greeting(msg, var):
	# print(var)
	return msg

# Loop indefinately
while(True):
	# Ask the user for input
	message = input("Ask the bot something (or enter \"quit\" to quit): ")

	# If the message is quit, then stop the loop
	if message == "quit": break

	# Get & print the response
	response = bot.query(message)
	print(response)

print("Program exited.")
