import sqlite3

class Request():
	def __init__(self, req_type, uname, uid, pubkey, **kwargs):
		self.type = req_type
		self.username = uname
		self.userID = uid
		self.pubkey = pubkey
		self.arguments = **kwargs

	def post_req():
		conn = sqlite3.connect(self.arguments.db)
		c = conn.cursor()

		q = "INSERT INTO TABLE {} VALUES (?, ?, ?)".format(self.arguments.table)

		c.execute(q, (self.username, self.userID, self.pubkey))

		conn.commit()
		conn.close()
