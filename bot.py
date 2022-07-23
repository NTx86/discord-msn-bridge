import discord
import threading
import time
from Util import *
import asyncio
import urllib.parse
import config
import random

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as', self.user)

	async def on_message(self, message):
		# don't respond to ourselves
		if message.author == self.user:
			return
		
		for client in connected_clients:
			if connected_clients[client] == message.channel.id:
				SendMessage(client, message.content, f"{message.id}@discorduser.com", urllib.parse.quote(str(message.author)))
			
	async def sendmessage(self, message, discordid):
		channel = client.get_channel(discordid)
		await channel.send(message)
		
	async def getchannels(self):
		text_channel_list = []
		for guild in client.guilds:
			for channel in guild.text_channels:
				text_channel_list.append(channel)
		return text_channel_list
			
			
def send_my_message(message,discordid):
	global client
	asyncio.run_coroutine_threadsafe(client.sendmessage(message,discordid), client.loop)
	
def bot_get_channels():
	global client
	text_channel_list = asyncio.run(client.getchannels())
	return text_channel_list
			
def startbot():
	global client
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	intents = discord.Intents.default()

	client = MyClient(intents=intents)
	client.run(config.discordtoken)

Botthread = threading.Thread(target=startbot)