from Util import *
import requests
import time
from bot import send_my_message

def GetUserFriendsByEmailList(email):
	return {"stub@stub.com":"stub",
			"stub2@stub.com":"stub2"}

def GetUserInfoByEmail(email):
	if email == "noob@hotmail.com":
		return {"email":"noob@hotmail.com",
				"nickname":"MSNUser",
				"status":"NLN",
				"version":0,
				"msnver":2}
	elif email == "stub@stub.com":
		return {"email":"stub@hotmail.com",
				"nickname":"stub",
				"status":"NLN",
				"version":0,
				"msnver":2}
	elif email == "stub2@stub.com":
		return {"email":"stub2@hotmail.com",
				"nickname":"stub2",
				"status":"NLN",
				"version":0,
				"msnver":2}

				
def OnMSGRecieve(conn, msg): #https://discord.com/api/webhooks/999991447086440458/potBKZv_2LdtI87OHi3lc-HUo5CYXQQPxVC5Oolv8g3Uwe9NOFExseOCDc5cwiFX7Wqb
	send_my_message(msg)
	#WebhookSend(msg, "https://discord.com/api/webhooks/999991447086440458/potBKZv_2LdtI87OHi3lc-HUo5CYXQQPxVC5Oolv8g3Uwe9NOFExseOCDc5cwiFX7Wqb")
	#SendMessage(conn,msg,"stub@stub.com","stub")