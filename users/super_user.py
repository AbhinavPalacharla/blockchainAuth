from user import User
import ed25519 as e
import json
import sqlite3

class SuperUser(User):

	def __init__(self, uname, passwd):
		super().__init__(uname, passwd)
		self.rank = 4

	def accept_join_request(self, targetID):
		msg = {
			'response': True
		}

		sig = self.gen_signature(msg)
		conn = sqlite3.connect('requests.db')
		c = conn.cursor()
		c.execute("""INSERT INTO acc_req VALUES (?, ?, ?, ?, ?, ?)""", (self.username, self.userID, targetID, self.pubkeyObj, json.dumps(msg).encode('utf-8'), sig))
		conn.commit()
		conn.close()

if __name__=='__main__':
	suA = SuperUser('abhi_admin', 'admin_passwd')
	suA.userID = 1111
	print(suA.userID)
	suA.accept_join_request(6666)

	suB = SuperUser('abhi_admin1', 'admin_passwd')
	suB.userID = 2222
	print(suB.userID)
	suB.accept_join_request(6666)
