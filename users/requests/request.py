import sqlite3
import sys

class Request():
	def __init__(self, uname, uid, pubkey):
		self.username = uname
		self.userID = uid
		self.pubkey = pubkey
		self.isVerified = self.checkVerification()

	def checkVerification(self):
		conn = sqlite3.connect('verified_users.db')
		c = conn.cursor()

		c.execute("""SELECT * FROM users WHERE userID=?""", (self.userID,))
		resp = c.fetchall()

		if len(resp) != 0:
			return True
		elif len(resp) == 0:
			return False
		else:
			print("something went wrong..")
			sys.exit(1)
