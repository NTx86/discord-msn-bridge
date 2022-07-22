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
				
def WebhookSend(message,webhook):
	success = 0
	ratelimited = 1
	unknown = 2
	exception = 3
	try:
		myobj = {'content': message,
			'username': "MSN Messenger 3.6",
			'avatar_url':"https://cdn.discordapp.com/attachments/765909592734957578/999992945337962566/Capture.PNG"}
		r = requests.post(webhook,data=myobj)
		if 'rate limited' in r.text:
			print(r.text)
			time.sleep(20)
			#WebhookSend(message,webhook)
			return ratelimited
		elif r.text == "":
			return success
		else:
			print(r.text)
			time.sleep(10)
			#WebhookSend(message,webhook)
			return unknown
	except Exception as e:
		print(e)
		time.sleep(1)
		return exception
				
def OnMSGRecieve(conn, msg): #https://discord.com/api/webhooks/999991447086440458/potBKZv_2LdtI87OHi3lc-HUo5CYXQQPxVC5Oolv8g3Uwe9NOFExseOCDc5cwiFX7Wqb
	send_my_message(msg)
	#WebhookSend(msg, "https://discord.com/api/webhooks/999991447086440458/potBKZv_2LdtI87OHi3lc-HUo5CYXQQPxVC5Oolv8g3Uwe9NOFExseOCDc5cwiFX7Wqb")
	#SendMessage(conn,msg,"stub@stub.com","stub")