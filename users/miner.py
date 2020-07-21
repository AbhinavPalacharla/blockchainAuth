import sqlite3
import sys
import uuid
import ed25519
import json
from requests.verify_identify_request import VerifyIdentityRequest
import pickle


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
		try:
			pubkey.verify(sig, json.dumps(msg).encode('utf-8'), encoding='hex')
			return json.loads(msg.decode('utf-8'))
		except:
			print("Error: integrity could not be verified, data may have been tampered with..")
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

			sig = self.gen_signature(data)

			c.execute("""INSERT INTO verif_ident VALUES (?, ?, ?, ?, ?, ?)""", (self.username, self.userID, i[2], self.pubkeyObj, json.dumps(data), sig))
			conn.commit()
		print('done')
if __name__ == '__main__':
	m = Miner('miner1')
	m.userID = 4444
	m.handle_verification()
