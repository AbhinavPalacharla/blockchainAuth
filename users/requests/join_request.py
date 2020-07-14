import sqlite3
from .request import Request

class JoinRequest(Request):
	def __init__(self, uname, uid, pubkey, endorser1, endorser2, endorser3):
		super().__init__('join', uname, uid, pubkey)
		self.end1ID = endorser1
		self.end2ID = endorser2
		self.end3ID = endorser3


	def post_req(self):
		conn = sqlite3.connect('requests.db')
		c = conn.cursor()

		c.execute("INSERT INTO join_req VALUES (?, ?, ?, ?, ?, ?)", (self.username, self.userID, self.pubkey, self.end1ID, self.end2ID, self.end3ID))
		#c.execute(self.payload, self.insert_args)

		conn.commit()
		conn.close()
