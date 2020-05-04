# Basic Python Chatbot
This is a very rudamentary chatbot built in Python. It's built for single sentence inputs & uses a very basic implementation of text classification. The more data it has, the more accurate it'll be.

### Setup
Setup is *very* simple. All it takes is importing the Chatbot class and then making an instance of it. That's really it.
```py
from chatbot import Chatbot

bot = Chatbot()
```

Now you may be wondering, "how is it getting the data?" and that's quite simple as well. By default, it looks for data in the `./intents` folder. It will look through any json file to check if there's data that it can use there.

```json
{
	"name": "intent_name",
	"data": ["array of common inputs for this intent"],
	"responses": ["array of responses"]
}
```

Now, with all that said and done how do we ask the bot something? Once again, it's very that simple:

```py
response = bot.query("message")
```