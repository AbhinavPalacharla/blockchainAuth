import uuid
import ed25519
import json
from requests.poke_request import PokeRequest
from requests.verify_response_request import VerifyReponseRequest
import sys
from cryptography.fernet import Fernet
import sqlite3

class User():

	def __init__(self, uname, passwd):
		self.username = uname
		self.password = self.encrypt(passwd)
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
		#print(f"priv: {self.privkey.to_ascii(encoding='hex')}")
		#print(f"pub: {self.pubkey.to_ascii(encoding='hex')}")

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

	def request_verification(self):
		conn = sqlite3.connect('verify_user_req.db')
		c = conn.cursor()

		p = PokeRequest(self.username, self.userID, self.pubkey)

		resp = None

		while (resp == None) or (c.rowcount() == 0):
			c.execute("""SELECT * FROM verif_ident WHERE targetID=?""", (self.userID,))
			resp = c.fetchall()

		dr = self.verify(resp[0][5]. resp[0][4], resp[0][3])

		resp = None

		data = {
			"uniqe_num": dr.unique_num
		}

		sig = self.gen_signature(data)

		c.execute("""INSERT INTO resp  VALUES (?, ?, ?, ?, ?)""", (self.username, self.userID, resp[0][1], self.pubkey, self.sig))

		while (resp == None) or (c.rowcount() == 0):
			c.execute("""SELECT * FROM verif_ident WHERE targetID=?""", (self.userID,))
			resp = c.fetchall()

		if resp[0][3] == 'verified':
			print('account verified successfully')
		else:
			print('account could not be verified: exiting..')
			sys.exit(1)

		conn.close()


if __name__ == '__main__':
	pass
	'''
	u = User('abhi', 'abhipasswd')
	data = {
		"message": "accept",
		"rank": 4
	}
	sig = u.gen_signature(data)

	print(u.pubkey.verify(sig, json.dumps(data).encode('utf-8'), encoding='hex'))

	try:
		u.pubkey.verify(sig, json.dumps(data).encode('utf-8'), encoding='hex')
		print("good")
	except:
		print("not good")
	'''

	u = User('abhi', 'abhipasswd')
	print(u.password)
