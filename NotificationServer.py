import socket
from Util import *
from Backend import *
import config
import random
import MSNSession
import threading

MSNPversions = {"MSNP2":2,
				"MSNP3":3,
				"MSNP4":4,
				"MSNP5":5,
				"MSNP6":6,
				"MSNP7":7,
				"MSNP8":8,
				"MSNP9":9,
				"MSNP10":10}

def NF_VER(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	ver = cmdarg[2]
	if not ver in MSNPversions:
		ver = "MSNP10"
	safesend(conn, f"VER {sync} {ver} CVR0")
	userinfo["msnver"] = MSNPversions[ver]
	return 0
	
def NF_INF(conn,data,userinfo):
	if userinfo["msnver"] == None:
		return 1
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	safesend(conn,f"INF {sync} MD5")
	return 0
	
def NF_USR(conn,data,userinfo):
	if userinfo["msnver"] == None:
		return 1
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	email = userinfo["email"]
	if cmdarg[2] == 'MD5':
		if cmdarg[3] == "I":
			email = cmdarg[4].lower()
			if MSNSession.DoesSessionExists(email):
				senderror(conn, sync, 207) #Already logged in
				return 2
			safesend(conn,f"USR {sync} MD5 S 1013928519.693957190")
			print("sent a challenge")
			userinfo["session"] = {} #this will be our session
			userinfo["session"]["email"] = email
			userinfo["session"]["version"] = random.randint(1,1000) #random
			userinfo["session"]["nickname"] = "MSNuser"
			userinfo["email"] = email #for internal session
			userinfo["authstage"] = True
			return 0
		if cmdarg[3] == "S":
			#usrdata = getuserdata(email)
			if userinfo["authstage"] == False:
				return 1
			passwordmd5sent = cmdarg[4]
			if passwordmd5sent == GenerateMD5password(config.MSN_password, "1013928519.693957190"):
				nickname = userinfo["session"]["nickname"]
				MSNSession.CreateSession(email, userinfo["session"])
				del userinfo["session"] #delete the session from internal session as we dont need it anymore
				userinfo["cmdwlist"] = []
				safesend(conn, f"USR {sync} OK {email} {nickname}")
				print("auth complete")
			else:
				senderror(conn,sync,911)
				return 2
			return 0
	elif cmdarg[2] == 'TWN':
		if cmdarg[3] == "I":
			email = cmdarg[4].lower()
			if MSNSession.DoesSessionExists(email):
				senderror(conn, sync, 207) #Already logged in
				return 2
			safesend(conn,f"USR {sync} TWN S ct=1312946236,rver=6.1.6206.0,wp=FS_40SEC_0_COMPACT,lc=1033,id=507,ru=http:%2F%2Fmessenger.msn.com,tw=0,kpp=1,kv=4,ver=2.1.6000.1,rn=1lgjBfIL,tpf=b0735e3a873dfb5e75054465196398e0")
			print("sent a challenge")
			userinfo["session"] = {} #this will be our session
			userinfo["session"]["email"] = email
			userinfo["session"]["version"] = random.randint(1,1000) #random
			userinfo["session"]["nickname"] = "MSNuser"
			userinfo["email"] = email #for internal session
			userinfo["authstage"] = True
			return 0
		if cmdarg[3] == "S":
			#usrdata = getuserdata(email)
			if userinfo["authstage"] == False:
				return 1
			TWMsent = cmdarg[4]
			if MSNSession.ReadKey(TWMsent) != None:
				nickname = userinfo["session"]["nickname"]
				MSNSession.CreateSession(email, userinfo["session"])
				del userinfo["session"] #delete the session from internal session as we dont need it anymore
				userinfo["cmdwlist"] = []
				if userinfo["msnver"] == 9:
					safesend(conn, f"USR {sync} OK {email} {nickname} 1 0")
				elif userinfo["msnver"] >=10:
					safesend(conn,f"USR {sync} OK {email} 1 0")
				else:
					safesend(conn, f"USR {sync} OK {email} {nickname}")
				print("auth complete")
			else:
				senderror(conn,sync,911)
				return 2
			return 0
	return 1
			
def NF_SYN(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	if userinfo["msnver"] < 10:
		sentversion = int(cmdarg[2])+1
		safesend(conn, f"SYN {sync} {sentversion}") #first response
		
		#privacy settings
		safesend(conn, f"GTC {sync} {sentversion} A")
		safesend(conn, f"BLP {sync} {sentversion} AL")
		safesend(conn, f"BLP {sync} {sentversion} AL")
		#usergroup
		usergroup = -1
		if userinfo["msnver"] >= 7:
			safesend(conn, f"LSG {sync} {sentversion} 1 1 0 Other%20Contacts 0")
		#user list
		userlist = GetUserFriendsByEmailList(userinfo["email"])
		#foward list
		SendOutLST(conn,sync,"FL",sentversion,userlist,usergroup)
		#some list
		SendOutLST(conn,sync,"AL",sentversion,userlist,-1)
		#block list
		safesend(conn, f"LST {sync} BL {sentversion} 0 0")
		#reverse list
		SendOutLST(conn,sync,"RL",sentversion,userlist,-1)
		
		#send online statuses
		currentcount = 1
		for user in userlist:
			email = user
			nickname = userlist[user]
			safesend(conn, f"ILN {sync} NLN {email} {nickname}")
			currentcount += 1
	else:
		nickname = MSNSession.GetSession(userinfo["email"])["nickname"]
		safesend(conn, f"SYN {sync} 2005-04-23T18:57:44.8130000-07:00 2005-04-23T18:57:54.2070000-07:00 3 0")
		#privacy settings
		safesend(conn, f"GTC A")
		safesend(conn, f"BLP AL")
		safesend(conn, f"PRP MFN {nickname}")
		#user list
		userlist = GetUserFriendsByEmailList(userinfo["email"])
		SendOutLST10(conn,userlist)
		
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
	safesend(conn, f"CVR {sync} 0 0 0  http://messenger.hotmail.com/mmsetup.exe ")
	return 0
	
def NF_XFR(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	key = random.randint(0, 999999999)
	session = MSNSession.GetSession(userinfo['email'])
	if session == None:
		return 1
	MSNSession.CreateKey(key,session)
	print("XFR redirecting to switchboard")
	safesend(conn, f"XFR {sync} SB {config.server}:{config.SB_port} CKI {key}")
	
def NF_OUT(conn,data,userinfo):
	return 2
	
def NF_REA(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	useremail = cmdarg[2]
	usernamechg = cmdarg[3]
	email = userinfo['email']
	if useremail == email:
		session = MSNSession.GetSession(email)
		with threading.Lock():
			session["nickname"] = usernamechg
	safesend(conn, f"REA {sync} 19 {useremail} {usernamechg}")
	
def NF_PNG(conn,data,userinfo):
	safesend(conn,"QNG 50")
	
def NF_URL(conn,data,userinfo):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	safesend(conn,f"URL {sync} unknown http://www.example.com")

NF_cmds = {"VER": NF_VER,
			"INF": NF_INF,
			"USR": NF_USR,
			"SYN": NF_SYN,
			"CHG": NF_CHG,
			"CVR": NF_CVR,
			"XFR": NF_XFR,
			"OUT": NF_OUT,
			"REA": NF_REA,
			"PNG": NF_PNG,
			"URL": NF_URL}