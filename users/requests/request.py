import sqlite3

class Request():
	def __init__(self, uname, uid, pubkey, **kwargs):
		self.username = uname
		self.userID = uid
		self.pubkey = pubkey
		
