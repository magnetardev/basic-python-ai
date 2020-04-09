from random import choice
import datetime

handlers = {}

# This creates a decorator named "intent"
# tl;dr: It will automatically add the function to the handlers 
# 		 dictionary to make accessing the methods simpler.
#
# Usage: 
# @intent
# def intent_name():
# 	...
intent = lambda f: handlers.setdefault(f.__name__, f)

@intent
def unknown(string):
	res = choice(['I don\'t know what you said there...', 'I\'m not sure what to say...', 'Come again?', 'I don\'t know how to answer that.'])
	return res

@intent
def greeting(string):
	res = choice(['Hello there!', 'Hello!', 'Hello to you too!', 'Hey!'])
	return res


@intent
def time(string):
	return f"The time is {datetime.datetime.now().time()} right now."