import socket
import threading
from Util import *
import config
import random
import MSNSession

printdebug = False

def ParseHTTP(conn,data):
	headers = {}
	lines = data.split("\r\n")
	request = lines[0].split(" ")
	lines = lines[1:]
	for line in lines:
		Args = line.split(":")
		if len(Args) < 2: break
		HeaderName, HeaderArg = Args[0], ''.join(Args[1:])[1:]
		headers[HeaderName] = HeaderArg
	msg = data.split("\r\n\r\n")
	if len(msg) >= 2:
		msg = msg[1]
	else:
		msg = ""
	return request, headers, msg
	
def constructhttp(uheaders, content):
	construct = ""
	headers = {"Accept-Ranges":"bytes",
				"Connection":"Closed"}
	headers = {**headers, **uheaders}
   
	construct = construct + "HTTP/1.1 200 OK\r\n"
	headerstr = ""
	for header in headers:
		headerstr += header + ": " + headers[header] + "\r\n"

	construct = construct + headerstr + '\r\n' + content + '\n'
	return construct

def WS_connected(conn, addr):
	BUFFER_SIZE = 1024
	try:
		while 1:
			data = conn.recv(BUFFER_SIZE)
			if not data: break
			data = data.decode('utf-8')[:-2]
			request, headers, msg = ParseHTTP(conn,data)
			if printdebug == True:
				print(headers)
			if request[1] == "/rdr/pprdr.asp":
				safesend(conn, constructhttp({"PassportURLs":f"DALogin=http://{config.server}/login"},""),printdebug,False)
			elif request[1] == "/login":
				password = headers['Authorization'].split(",")[3].split("=")[1]
				if config.MSN_password == password:
					token = str(random.randint(0,9999999999))+"."+str(random.randint(0,9999999999))
					MSNSession.CreateKey(token,headers)
					safesend(conn, constructhttp({"Authentication-Info": f"Passport1.4 da-status=success,from-PP='{token}'"},""),printdebug,False)
				else:
					placeholder = 0 #i have no documentation on what to do if it fails
			else:
				safesend(conn, constructhttp({"Content-Type":"text/html; charset=iso-8859-1"},"404 API not found"),printdebug,False)
			conn.close()
		conn.close()
	except socket.error as e:
		conn.close()
	finally:
		conn.close()

def startlisteningWS():
	while 1:
		TCP_IP = '0.0.0.0'
		TCP_PORT = 80
		BUFFER_SIZE = 1024
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((TCP_IP, TCP_PORT))
		s.listen(1)

		conn, addr = s.accept()
		print('Connection address:', addr)
		thread = threading.Thread(target=WS_connected,args=(conn, addr,))
		thread.start()