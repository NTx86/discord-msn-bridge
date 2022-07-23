import socket
import threading
from NotificationServer import NF_cmds 
from SwitchboardServer import SB_cmds
from Util import *
from bot import startbot, Botthread


def connected(conn,addr, srvcmds):
	email, username, status, version, msnver = 1,2,3,4,5
	userinfo = {"email":"blank@hotmail.com",
				"nickname":"MSNUser",
				"status":"NLN",
				"version":0,
				"msnver":2}
	try:
		while 1:
			data = conn.recv(BUFFER_SIZE)
			if not data: break
			#print("received data:", data)
			cmds = data.decode('utf-8').splitlines()
			for command in cmds:
				print(f"C>S: {command}")
				cmdarg = command.split(' ')
				if len(cmdarg) > 1: sync = cmdarg[1] 
				else: sync = "1"
				cmd = cmdarg[0]
				if cmd in srvcmds:
					cstatus = srvcmds[cmd](conn,command,userinfo)
					if cstatus == 1:
						senderror(conn,sync,500)
						conn.close()
						break
					elif cstatus == 2:
						conn.close()
						break
					continue
				else:
					if len(cmdarg) > 1: sync = cmdarg[1] 
					else: sync = "1"
					senderror(conn,sync,500)
					conn.close()
		conn.close()
	except socket.error as e:
		#sendtoallfriends(email,f"ILN 1 FLN {email} {username}")
		#if email in clients:
		#	del clients[email]
		conn.close()
	finally:
		#sendtoallfriends(email,f"ILN 1 FLN {email} {username}")
		#if email in clients:
		#	del clients[email]
		conn.close()

def SB_connected(conn,addr, srvcmds):
	email, username, status, version, msnver = 1,2,3,4,5
	userinfo = {"email":"blank@hotmail.com",
				"nickname":"MSNUser",
				"status":"NLN",
				"version":0,
				"msnver":2}
	try:
		while 1:
			data = conn.recv(BUFFER_SIZE)
			if not data: break
			#print("received data:", data)
			command = data.decode('utf-8')[:-2]
			#for command in cmds:
			print(f"C>S: {command}")
			cmdarg = command.split(' ')
			if len(cmdarg) > 1: sync = cmdarg[1] 
			else: sync = "1"
			cmd = cmdarg[0]
			if cmd in srvcmds:
				cstatus = srvcmds[cmd](conn,command,userinfo,data)
				if cstatus == 1:
					RemoveClient(conn)
					conn.close()
					break
				elif cstatus == 2:
					RemoveClient(conn)
					conn.close()
					break
				continue
			else:
				if len(cmdarg) > 1: sync = cmdarg[1] 
				else: sync = "1"
				RemoveClient(conn)
				conn.close()
		conn.close()
	except socket.error as e:
		RemoveClient(conn)
		conn.close()
	finally:
		RemoveClient(conn)
		conn.close()

def startlisteningSB():
	while 1:
		TCP_IP = '0.0.0.0'
		TCP_PORT = 53641
		BUFFER_SIZE = 1024
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((TCP_IP, TCP_PORT))
		s.listen(1)

		conn, addr = s.accept()
		print('Connection address:', addr)
		thread = threading.Thread(target=SB_connected,args=(conn, addr, SB_cmds))
		thread.start()
		#connectedSB()

SBthread = threading.Thread(target=startlisteningSB)
SBthread.start()
Botthread.start()

while 1:
	TCP_IP = '0.0.0.0'
	TCP_PORT = 1863
	BUFFER_SIZE = 1024

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	print(f"start listen {TCP_IP} {TCP_PORT}")
	s.listen(1)

	conn, addr = s.accept()
	print('Connection address:', addr)
	thread = threading.Thread(target=connected,args=(conn, addr, NF_cmds))
	thread.start()
