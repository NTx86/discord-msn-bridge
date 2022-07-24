import socket
from Util import *
from Backend import *
import MSNSession

def SB_USR(conn,data,conninfo,raw):
	cmdarg = data.split(' ')
	sync, email, key = cmdarg[1],cmdarg[2],cmdarg[3]
	userdata = MSNSession.ReadKey(int(key))
	email, nickname = userdata['email'], userdata['nickname']
	conninfo["email"] = email
	MSNSession.CreateSBsession(conn,"")
	conninfo["cmdwlist"] = []
	safesend(conn, f"USR {sync} OK {email} {nickname}")
	
def SB_CAL(conn,data,conninfo,raw):
	cmdarg = data.split(' ')
	sync = cmdarg[1]
	callemail = cmdarg[2]
	calluserinfo = GetUserInfoByEmail(callemail)
	conninfo["discordid"] = calluserinfo['discordid']
	MSNSession.ChangeSBsession(conn,calluserinfo['discordid'])
	safesend(conn, f"CAL {sync} RINGING 1337")
	safesend(conn, f"JOI {callemail} {calluserinfo['nickname']}")

def SB_MSG(conn,data,conninfo,raw):
	raw = raw.decode('utf-8')
	cmdarg = raw.split(' ')
	sync = cmdarg[1]
	ack = cmdarg[2]
	msglen = cmdarg[3]
	headers,msg = ParseMessage(raw)
	print(headers)
	if "text/plain" in headers["Content-Type"]:
		if msg != "\r\n":
			OnMSGRecieve(conn,msg,conninfo)
	return 0 #stub
	
def SB_OUT(conn,data,conninfo,raw):
	return 2


SB_cmds = {"USR": SB_USR,
			"CAL": SB_CAL,
			"MSG": SB_MSG,
			"OUT": SB_OUT}