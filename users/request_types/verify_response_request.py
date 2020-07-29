from .request import Request

class VerifyReponseRequest(Request):

	def __init__(self, uname, uid, pubkey, signature):
		super().__init__(uname, uid, pubkey)

	def post_req(self):
		conn = sqlite3.connect('verify_usr_req.db')
		c = conn.cursor()

		c.execute("INSERT INTO resp VALUES (?, ?, ?, ?)", (self.uname, self.uid, self.pubkey, self.signature))

		conn.commit()
		conn.close()
