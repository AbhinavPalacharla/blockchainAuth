from request import Request

class VerifyRequest(Request):

	def __init__(self, uname, uid, pubkey, signature):
		super().__init__('initial verify', uname, uid, pubkey):

	def post_req(self):
		conn = sqlite3.connect('verify_req.db')
		c = conn.cursor()

		c.execute("INSERT INTO verif_req VALUES (?, ?, ?, ?)", (self.uname, self.uid, self.pubkey, self.signature))

		conn.commit()
		conn.close()
