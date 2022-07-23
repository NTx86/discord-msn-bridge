from Util import *
import requests
import time
import bot

def GetUserFriendsByEmailList(email):
	friendlist = {}
	channels = bot.bot_get_channels()
	for channel in channels:
		friendlist[str(channel.id)+"@discord.com"] = channel.name
	print(channels)
	return friendlist
	#return {"general@discord.com":"#general"}

def GetUserInfoByEmail(email):
	channels = bot.bot_get_channels()
	id = email.split("@")[0]
	nickname = ""
	if check_int(id) == True:
		for channel in channels:
			if int(id) == channel.id:
				nickname = channel.name
		return {"email":email,
				"nickname":nickname,
				"discordid":int(id)}
	else:
		return {"email":email,
				"nickname":"MSNuser"}
				
def OnMSGRecieve(conn, msg, userinfo):
	bot.send_my_message(msg,userinfo['discordid'])
