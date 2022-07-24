import socket
from Util import *
from Backend import *

def SB_USR(conn,data,userinfo,raw):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	userinfo["email"] = cmdarg[2]
	userinfo["nickname"] = GetUserInfoByEmail(cmdarg[2])["nickname"]
	email, nickname = userinfo['email'], userinfo['nickname']
	connected_clients[conn] = ""
	safesend(conn, f"USR {sync} OK {email} {nickname}")
	
def SB_CAL(conn,data,userinfo,raw):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	callemail = cmdarg[2]
	calluserinfo = GetUserInfoByEmail(callemail)
	userinfo["discordid"] = calluserinfo['discordid']
	connected_clients[conn] = calluserinfo['discordid']
	safesend(conn, f"CAL {sync} RINGING 1337")
	safesend(conn, f"JOI {callemail} {calluserinfo['nickname']}")

def SB_MSG(conn,data,userinfo,raw):
	raw = raw.decode('utf-8')
	cmdarg = raw.split(' ')
	sync = cmdarg[1]
	ack = cmdarg[2]
	msglen = cmdarg[3]
	headers,msg = ParseMessage(raw)
	print(headers)
	if "text/plain" in headers["Content-Type"]:
		if msg != "\r\n":
			OnMSGRecieve(conn,msg,userinfo)
	return 0 #stub
	
def SB_OUT(conn,data,userinfo,raw):
	RemoveClient(conn)
	return 2


SB_cmds = {"USR": SB_USR,
			"CAL": SB_CAL,
			"MSG": SB_MSG,
			"OUT": SB_OUT}