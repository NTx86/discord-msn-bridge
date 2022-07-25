import threading
MSN_sessions = {}
MSN_keys = {}
SB_sessions = {}

#MSN Session functions

def RemoveSession(key):
	with threading.Lock():
		MSN_sessions.pop(key, None)
	
def CreateSession(key, data):
	with threading.Lock():
		MSN_sessions[key] = data
		
def ChangeSession(key, data):
	with threading.Lock():
		if key in MSN_sessions:
			MSN_sessions[key] = data
		
def GetSession(key):
	with threading.Lock():
		if key in MSN_sessions:
			return MSN_sessions[key]
		else:
			return None
	
def DoesSessionExists(key):
	with threading.Lock():
		if key in MSN_sessions:
			return True
		return False
	
#Switchboard Session functions

def RemoveSBsession(conn):
	with threading.Lock():
		SB_sessions.pop(conn, None)
	
def CreateSBsession(key, data):
	with threading.Lock():
		SB_sessions[key] = data
		
def ChangeSBsession(key, data):
	with threading.Lock():
		if key in SB_sessions:
			SB_sessions[key] = data
		
def GetSBsession(key):
	with threading.Lock():
		if key in SB_sessions:
			return SB_sessions[key]
		else:
			return None
	
def DoesSBsessionExists(key):
	with threading.Lock():
		if key in SB_sessions:
			return True
		return False
	
#Authkey Session functions

def CreateKey(key, data):
	with threading.Lock():
		MSN_keys[key] = data
		
def ReadKey(key):
	with threading.Lock():
		if key in MSN_keys:
			ret = MSN_keys[key]
			MSN_keys.pop(key, None)
			return ret
		else:
			return None