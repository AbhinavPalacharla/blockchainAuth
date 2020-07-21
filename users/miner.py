import sqlite3
import sys
import uuid
import ed25519
import json
from requests.verify_identify_request import VerifyIdentityRequest
import pickle
import time


class Miner():

	def __init__(self, uname):
		self.username = uname
		self.userID = self.gen_uniq_id()
		self.pubkey = None
		self.privkey = None

		self.gen_keys()


	def encrypt(self, passwd):
		#pass #implement later, need to use external lib for encryption
		encoded = passwd.encode()
		#f = Fernet(key)
		f = open('key.key', 'rb')
		key = f.read()
		f.close()

		fern = Fernet(key)
		encrypted = fern.encrypt(encoded)

		return encrypted


	def gen_keys(self):
		self.privkey, self.pubkey = ed25519.create_keypair()
		self.pubkeyObj = pickle.dumps(self.pubkey)
		self.privkeyObj = pickle.dumps(self.privkey)

	def gen_uniq_id(self):
		return (uuid.uuid1()).hex

	def gen_signature(self, data):
		msg = json.dumps(data).encode('utf-8')
		sig = self.privkey.sign(msg, encoding='hex')
		print(sig)
		return sig

	def verify(self, sig, msg, pubkey):

		print(f"message: {json.loads(msg)}")
		print(f"signature: {sig}")
		print(f"pubkey: {pubkey}")
		print(pubkey.verify(sig, json.dumps(json.loads(msg)).encode('utf-8'), encoding='hex'))

		try:
			pubkey.verify(sig, json.dumps(json.loads(msg)).encode('utf-8'), encoding='hex')
			print("verified")
			return json.loads(msg)
		except:
			print("Error: integrity could not be verified, data may have been tampered with..")
			e = sys.exc_info()[0]
			print(e)
			return False

	def handle_verification(self):
		conn = sqlite3.connect('verify_user_req.db')
		c = conn.cursor()

		c.execute("""SELECT * FROM init_verif_req""")
		resp = c.fetchall()
		print(resp)

		for i in resp:

			data = {
				"unique_num": (uuid.uuid1()).hex
			}

			print(data)

			c.execute("""INSERT INTO answers VALUES (?, ?)""", (i[2], data.get("unique_num")))
			conn.commit()

			sig = self.gen_signature(data)

			c.execute("""INSERT INTO verif_ident VALUES (?, ?, ?, ?, ?, ?)""", (self.username, self.userID, i[2], self.pubkeyObj, json.dumps(data), sig))
			conn.commit()

		print('waiting..')
		time.sleep(10)
		print('done waiting')

		c.execute("""SELECT * FROM resp""")
		resp = c.fetchall()
		print(resp)

		conn.close()

		for i in resp:
			conn = sqlite3.connect('verify_user_req.db')
			c = conn.cursor()
			c.execute("""SELECT * FROM answers WHERE userID=?""", (i[1],))
			answer = c.fetchall()
			print(f"answer: {answer}")

			ur = self.verify(i[5], i[4], pickle.loads(i[3]))
			print("ur: ")
			print(ur)
			print("unique num: ")
			print(ur.get("uniqe_num"))
			if ur.get("uniqe_num") == answer[0][1]:
				print(f"{i[1]} got the right answer")
				c.execute("""INSERT INTO result VALUES (?, ?, ?, ?)""", (self.username, self.userID, i[1], 'verified'))
				conn.commit()
				conn.close()
				conn = sqlite3.connect('verified_users.db')
				c = conn.cursor()
				c.execute("""INSERT INTO users VALUES (?, ?, ?)""", (i[0], i[1], i[3]))
				conn.commit()
				conn.close()
			elif ur.get("uniqe_num") != answer[0][1]:
				print(f"{i[1]} did not get the right answer")
				c.execute("""INSERT INTO result VALUES (?, ?, ?, ?)""", (self.username, self.userID, i[1], 'unverified'))
				conn.commit()
				conn.close()
			else:
				print("something went wrong...")

		print('done')

if __name__ == '__main__':
	m = Miner('miner1')
	m.userID = 4444
	m.handle_verification()
