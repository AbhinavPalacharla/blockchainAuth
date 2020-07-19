import sqlite3
from request import Request

class AcceptRequest(Request):

	def __init__(self, uname, uid, pubkey, target_id, signature):
		super().__init__(uname, uid, pubkey)

		self.targetID = target_id
		self.signature = signature

	def post_req(self):
		conn = sqlite3.connect(requests.db)
		c = conn.cursor()

		c.execute("""INSERT INTO acc_req VALUES (?, ?, ?, ?, ?)""", (self.username, self.userID, targetID, self.pubkey, self.signature))
