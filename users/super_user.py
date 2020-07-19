from user import User
import ed25519 as e
import json as j
import sqlite3

class SuperUser(User):

	def __init__(self, uname, passwd):
		super().__init__(uname, passwd)
		self.rank = 4

	def accept_join_request(self, accID):
		msg = b'accept'
		signature = self.privkey.sign(msg, encoding='hex')

		conn = sqlite3.connect('requests.db')
		c = conn.cursor()

		c.execute("INSERT INTO acc_req VALUES (?, ?, ?, ?)", (self.username, self.pubUserID, accID, signature))

		conn.commit()
		conn.close()

if __name__=='__main__':
	suA = SuperUser('abhi_admin', 'admin_passwd')
	suA.pubUserID = 1111
	print(suA.pubUserID)
	suA.accept_join_request(4444)

	suB = SuperUser('abhi_admin1', 'admin_passwd')
	suB.pubUserID = 2222
	print(suB.pubUserID)
	suB.accept_join_request(4444)
