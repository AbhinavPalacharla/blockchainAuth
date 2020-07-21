import uuid
import ed25519
import json
from requests.poke_request import PokeRequest
from requests.verify_response_request import VerifyReponseRequest
import sys
from cryptography.fernet import Fernet
import sqlite3
import time
import pickle

class TempUser():
#class for temporary user
	#def __init__(self, uname, request_role, endorser1, endorser2, endorser3):
	def __init__(self, uname, passwd, **kwargs):
		self.username = uname
		self.password = self.encrypt(passwd)
		self.userID = self.gen_uniq_id()
		self.pubkey = None
		self.privkey = None
		self.pubkeyObj = None
		self.privkeyObj = None
		self.arguments = kwargs
		#self.request_role = request_role
		#self.end1ID = endorser1
		#self.end2ID = endorser2
		#self.end3ID = endorser3

		self.gen_keys()

	def gen_keys(self):
		self.privkey, self.pubkey = ed25519.create_keypair()
		self.pubkeyObj = pickle.dumps(self.pubkey)
		self.privkeyObj = pickle.dumps(self.privkey)

	def gen_signature(self, data):
		msg = json.dumps(data).encode('utf-8')
		sig = self.privkey.sign(msg, encoding='hex')
		print(sig)
		return sig

	def verify(self, sig, msg, pubkey):

		print(json.loads(msg))

		try:
			pubkey.verify(sig, json.dumps(json.loads(msg)).encode('utf-8'), encoding='hex')
			return json.loads(msg.decode('utf-8'))
		except:
			print("Error: integrity could not be verified, data may have been tampered with..")
			return False

	def encrypt(self, passwd):
		encoded = passwd.encode()
		f = open('key.key', 'rb')
		key = f.read()
		f.close()
		fern = Fernet(key)
		encrypted = fern.encrypt(encoded)

		return encrypted

	def gen_uniq_id(self):
		return (uuid.uuid1()).hex

	def request_join(self):
		jr = JoinRequest(
			self.username,
			self.pubUserID,
			self.request_role,
			self.pubkey.to_ascii(encoding='hex'),
			endorser1 = self.arguments.endorser1,
			endorser2 = self.arguments.endorser2,
			endorser3 = self.arguments.endorser3
			)

		jr.post_req()

	def request_verification(self):
		conn = sqlite3.connect('verify_user_req.db')
		c = conn.cursor()

		#p = PokeRequest(self.username, self.password, self.userID, self.pubkey.to_ascii(encoding='hex'))
		p = PokeRequest(self.username, self.password, self.userID, self.pubkeyObj)
		p.post_req()

		resp = []

		while (len(resp) == 0):
			c.execute("""SELECT * FROM verif_ident WHERE targetID=?""", (self.userID,))
			resp = c.fetchall()
			print(resp)
			time.sleep(2)

		dr = self.verify(resp[0][5], resp[0][4], resp[0][3])
		print(dr)
		resp = []

		time.sleep(6000)

		data = {
			"uniqe_num": dr.get(unique_num)
		}

		sig = self.gen_signature(data)

		c.execute("""INSERT INTO resp  VALUES (?, ?, ?, ?, ?)""", (self.username, self.userID, resp[0][1], self.pubkey, json.dumps(data).encode('utf-8'), self.sig))

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
	t = TempUser('abhi', 'passwd', request_rank=0, endorser1=1111, endorser2=2222, endorser3=3333)
	t.userID = 6666
	t.request_verification()
