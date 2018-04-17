import atexit
import random
import json
import os
from mattermost_bot.bot import listen_to
from mattermost_bot import settings

QUOTES = {}

def on_init():
	global QUOTES

	with open(settings.QUOTES_DB, 'r') as fp:
		QUOTES = json.load(fp)

	if settings.DEBUG:
		print('quotes: Loaded {} quotes'.format(len(QUOTES)))


@atexit.register
def on_exit():
	with open(settings.QUOTES_DB, 'w') as fp:
		json.dump(QUOTES, fp)


@listen_to('!(?:q(?:uote)? )?(\w+)')
def get_quote(message, name):
	name = name.lower()

	if name not in QUOTES:
		return

	q = QUOTES[name]
	message.reply(random.choice(q))


@listen_to('!a(?:dd)?q(?:uote)? (\w+) (.*)')
def add_quote(message, name, value):
	name = name.lower()

	quotes = QUOTES.get(name, [])
	quotes.append(value)
	QUOTES[name] = quotes

	message.react(':+1:')
