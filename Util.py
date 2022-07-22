import socket

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

def SendOutLST(conn,sync,mlist,sentversion,userlist):
	userlistcount = len(userlist)
	currentcount = 1
	for user in userlist:
		email = user
		nickname = userlist[user]
		safesend(conn, f"LST {sync} {mlist} {sentversion} {currentcount} {userlistcount} {email} {nickname}")
		currentcount += 1