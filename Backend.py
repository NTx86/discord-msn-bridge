def GetUserFriendsByEmailList(email):
	return {"stub@stub.com":"stub",
			"stub2@stub.com":"stub2"}

def GetUserInfoByEmail(email):
	if email == "noob@hotmail.com":
		return {"email":"noob@hotmail.com",
				"nickname":"MSNUser",
				"status":"NLN",
				"version":0,
				"msnver":2}
	elif email == "stub@stub.com":
		return {"email":"stub@hotmail.com",
				"nickname":"stub",
				"status":"NLN",
				"version":0,
				"msnver":2}
	elif email == "stub2@stub.com":
		return {"email":"stub2@hotmail.com",
				"nickname":"stub2",
				"status":"NLN",
				"version":0,
				"msnver":2}