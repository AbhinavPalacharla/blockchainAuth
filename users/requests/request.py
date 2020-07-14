import sqlite3

class Request():
	def __init__(self, req_type, uname, uid, pubkey, **kwargs):
		self.type = req_type
		self.username = uname
		self.userID = uid
		self.pubkey = pubkey
		self.arguments = kwargs
