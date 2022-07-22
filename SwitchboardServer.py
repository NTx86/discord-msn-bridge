import socket
from Util import *
from Backend import *

def constructmessage(msg,email,nickname,sync):
	command = ""
	msnpmsg = "MIME-Version: 1.0\r\n"
	msnpmsg += "Content-Type: text/plain; charset=UTF-8\r\n"
	msnpmsg += "X-MMS-IM-Format: FN=Arial; EF=; CO=0; CS=0; PF=22\r\n"
	msnpmsg += "\r\n"
	msnpmsg += msg
	msnplen = len(msnpmsg)
	command = f"MSG {email} {nickname} {msnplen}\r\n{msnpmsg}"
	print(command)
	return command
	

def SB_USR(conn,data,userinfo,raw):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	userinfo["email"] = cmdarg[2]
	userinfo["nickname"] = GetUserInfoByEmail(cmdarg[2])["nickname"]
	email, nickname = userinfo['email'], userinfo['nickname']
	safesend(conn, f"USR {sync} OK {email} {nickname}")
	
def SB_CAL(conn,data,userinfo,raw):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	callemail = cmdarg[2]
	safesend(conn, f"CAL {sync} RINGING 1337")
	safesend(conn, f"JOI {callemail} #general")

def SB_MSG(conn,data,userinfo,raw):
	raw = raw.decode('utf-8')
	cmdarg = raw.split(' ')
	sync = cmdarg[1]
	ack = cmdarg[2]
	msglen = cmdarg[3]
	safesend(conn, constructmessage("Hello World!","stub@stub.com","stub",sync))
	return 0 #stub
	
def SB_OUT(conn,data,userinfo,raw):
	return 2


SB_cmds = {"USR": SB_USR,
			"CAL": SB_CAL,
			"MSG": SB_MSG,
			"OUT": SB_OUT}