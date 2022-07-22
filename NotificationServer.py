import socket
from Util import *
from Backend import *

def NF_VER(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	safesend(conn, f"VER {sync} MSNP4 CVR0")
	userinfo["msnver"] = 4
	return 0
	
def NF_INF(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	safesend(conn,f"INF {sync} MD5")
	return 0
	
def NF_USR(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	email = userinfo["email"]
	if cmdarg[2] == 'MD5':
		if cmdarg[3] == "I":
			email = cmdarg[4].lower()
			safesend(conn,f"USR {sync} MD5 S 1013928519.693957190")
			print("sent a challenge")
			userinfo["email"] = email
			userinfo["version"] = 54 #random
			userinfo["nickname"] = ""
			return 0
		if cmdarg[3] == "S":
			#usrdata = getuserdata(email)
			passwordmd5sent = cmdarg[4]
			nickname = "MSNuser"
			safesend(conn, f"USR {sync} OK {email} {nickname}")
			print("auth complete")
			return 0
			
			
def NF_SYN(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	sentversion = int(cmdarg[2])+1
	safesend(conn, f"SYN {sync} {sentversion}") #first response
	#privacy settings
	safesend(conn, f"GTC {sync} {sentversion} A")
	safesend(conn, f"BLP {sync} {sentversion} AL")
	safesend(conn, f"BLP {sync} {sentversion} AL")
	#user list
	userlist = GetUserFriendsByEmailList(userinfo["email"])
	#foward list
	SendOutLST(conn,sync,"FL",sentversion,userlist)
	#some list
	SendOutLST(conn,sync,"AL",sentversion,userlist)
	#block list
	safesend(conn, f"LST {sync} BL {sentversion} 0 0")
	#reverse list
	SendOutLST(conn,sync,"RL",sentversion,userlist)
	#send online statuses
	currentcount = 1
	for user in userlist:
		email = user
		nickname = userlist[user]
		safesend(conn, f"ILN {sync} NLN {email} {nickname}")
		currentcount += 1
	
	return 0
	
def NF_CHG(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	status = cmdarg[2]
	safesend(conn, f"CHG {sync} {status}")
	return 0
	
def NF_CVR(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	safesend(conn, f"CVR {sync} 2.2.1053 2.2.1053 2.2.1053  http://messenger.hotmail.com/mmsetup.exe ")
	return 0
	
def NF_XFR(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	key = 1337 #if auth is needed then this will have to be replaced with a random num
	print("XFR redirecting to switchboard")
	safesend(conn, f"XFR {sync} SB 127.0.0.1:53641 CKI {key}")
	
def NF_OUT(conn,data,userinfo):
	return 2

NF_cmds = {"VER": NF_VER,
			"INF": NF_INF,
			"USR": NF_USR,
			"SYN": NF_SYN,
			"CHG": NF_CHG,
			"CVR": NF_CVR,
			"XFR": NF_XFR,
			"OUT": NF_OUT}