import sqlite3
import sys
import uuid
import ed25519
import json
from request_types.verify_identify_request import VerifyIdentityRequest
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
		#print(f"message: {json.loads(msg)}")
		#print(f"signature: {sig}")
		#print(f"pubkey: {pubkey}")
		#print(pubkey.verify(sig, json.dumps(json.loads(msg)).encode('utf-8'), encoding='hex'))
		try:
			pubkey.verify(sig, json.dumps(json.loads(msg)).encode('utf-8'), encoding='hex')
			print("verified")
			return json.loads(msg)
		except:
			print("Error: integrity could not be verified, data may have been tampered with..")
			e = sys.exc_info()[0]
			print(e)
			return False

	def handle_accept_request(self):
		conn = sqlite3.connect('requests.db')
		c = conn.cursor()

		c.execute("""SELECT * FROM join_req""")
		resp = c.fetchall()

		for i in resp:
			c.execute("""SELECT * FROM acc_req WHERE targetID=?""", (i[1],))
			acc_reqs = c.fetchall()

			if len(acc_reqs) < 2:
				continue

			#print('testing')
			#print(json.loads(acc_reqs[0][4]).encode('utf-8'))
			#print('end of testing')

			if (self.verify(acc_reqs[0][5], acc_reqs[0][4], pickle.loads(acc_reqs[0][3])) and self.verify(acc_reqs[0][5], acc_reqs[0][4], pickle.loads(acc_reqs[0][3]))):
				if ((json.loads(acc_reqs[0][4])).get('response') == True) and ((json.loads(acc_reqs[0][4])).get('response') == True):
					print('ready to accept') #placeholder

if __name__ == '__main__':
	m = Miner('miner1')
	m.handle_accept_request()
