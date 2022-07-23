from Util import *
import requests
import time
from bot import send_my_message

def GetUserFriendsByEmailList(email):
	return {"general@discord.com":"#general"}

def GetUserInfoByEmail(email):
	if email == "noob@hotmail.com":
		return {"email":"noob@hotmail.com",
				"nickname":"MSNUser",
				"status":"NLN",
				"version":0,
				"msnver":2}
	elif email == "general@discord.com":
		return {"email":"stub@hotmail.com",
				"nickname":"stub",
				"status":"NLN",
				"version":0,
				"msnver":2}

				
def OnMSGRecieve(conn, msg):
	send_my_message(msg)
