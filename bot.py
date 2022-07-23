import discord
import threading
import time
from Util import *
import asyncio
import urllib.parse
from config import discordtoken
import random

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as', self.user)
		channel = client.get_channel(999990934425047092)
		await channel.send('Bot started')

	async def on_message(self, message):
		# don't respond to ourselves
		if message.author == self.user:
			return

		SendMessage(connected_clients[0], message.content, f"stub{random.randint(0, 9999999)}@stub.com", urllib.parse.quote(str(message.author)))
		#if message.content == 'ping':
		#	await message.channel.send('pong')
			
	async def sendmessage(self, message):
		channel = client.get_channel(999990934425047092)
		await channel.send(message)
			
			
def send_my_message(message):
	global client
	asyncio.run_coroutine_threadsafe(client.sendmessage(message), client.loop)
			
def startbot():
	global client
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	intents = discord.Intents.default()
	#intents.message_content = True

	client = MyClient(intents=intents)
	client.run(discordtoken)

Botthread = threading.Thread(target=startbot)