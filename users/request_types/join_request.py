import sqlite3
from .request import Request

class JoinRequest(Request):
	def __init__(self, uname, uid, pubkey, request_rank, endorser1, endorser2, endorser3):
		super().__init__(uname, uid, pubkey)
		self.request_rank = request_rank
		self.end1ID = endorser1
		self.end2ID = endorser2
		self.end3ID = endorser3


	def post_req(self):
		conn = sqlite3.connect('requests.db')
		c = conn.cursor()

		c.execute("INSERT INTO join_req VALUES (?, ?, ?, ?, ?, ?, ?)", (self.username, self.userID, self.pubkey, self.request_rank, self.end1ID, self.end2ID, self.end3ID))
		print('loaded')
		conn.commit()
		conn.close()
		print('done')
