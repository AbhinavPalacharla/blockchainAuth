import sqlite3
from request import Request

class PokeRequest(Request):

	def __init__(self, uname, passwd, uid, pubkey):
		super().__init__(uname, uid, pubkey)
		self.passwd = passwd

	def post_req(self):
		conn = sqlite3.connect('verify_user_req.db')
		c = conn.cursor()

		c.execute("""INSERT INTO init_verif_req VALUES (?, ?, ?, ?)""", (self.username, self.passwd, self.userID, self.pubkey))

		conn.commit()
		conn.close()
