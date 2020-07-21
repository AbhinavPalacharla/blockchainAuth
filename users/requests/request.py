import sqlite3

class Request():
	def __init__(self, uname, uid, pubkey):
		self.username = uname
		self.userID = uid
		self.pubkey = pubkey
