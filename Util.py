import socket
import hashlib

connected_clients = {}

def safesend(socket,data):
	try:
		socket.send((data+"\r\n").encode())
		print(f"S>C: {data}")
	except Exception as e:
		print("socket send fail")
		print(e)
		
def senderror(socket,sync,errnum):
	errnum = str(errnum)
	safesend(socket, errnum+" "+sync)

def SendOutLST(conn,sync,mlist,sentversion,userlist,usergroup):
	userlistcount = len(userlist)
	currentcount = 1
	#msnp7 usergroup support
	if usergroup == -1:
		usergroup = ""
	else:
		usergroup = " "+str(usergroup)
	for user in userlist:
		email = user
		nickname = userlist[user]
		safesend(conn, f"LST {sync} {mlist} {sentversion} {currentcount} {userlistcount} {email} {nickname}{usergroup}")
		currentcount += 1
		
def constructmessage(msg,email,nickname):
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
	
def ParseMessage(raw):
	headers = {}
	lines = raw.split("\r\n")
	lines.pop(0) #delete the MSG command itself
	for line in lines:
		Args = line.split(":")
		if len(Args) != 2: break
		HeaderName, HeaderArg = Args[0], Args[1]
		headers[HeaderName] = HeaderArg
	msg = raw.split("\r\n\r\n")
	if len(msg) >= 2:
		msg = msg[1]
	else:
		msg = ""
	return headers, msg
	
def SendMessage(conn,msg,email,nickname):
	safesend(conn, constructmessage(msg,email,nickname))
	
def RemoveClient(conn):
	connected_clients.pop(conn, None)
		
def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()
	
def GenerateMD5password(password,challenge):
	concentrate = challenge+password
	md5 = hashlib.md5(concentrate.encode())
	return md5.hexdigest()
