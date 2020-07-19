import uuid
import ed25519 as e
from requests.join_request import JoinRequest
from requests.verify_request import VerifyRequest
from requests.request import Request

class temp():
#class for temporary user
	def __init__(self, uname, request_role, endorser1, endorser2, endorser3):
		self.username = uname
		self.pubUserID = self.gen_uniq_id()
		self.privUserID = self.gen_uniq_id()
		self.request_role = request_role
		self.end1ID = endorser1
		self.end2ID = endorser2
		self.end3ID = endorser3
		self.pubkey = None
		self.privkey = None

		self.gen_keys()

	def request_verification(self):
		r = Request('verify_request', self.username, self.pubUserID, self.pubkey, db='verif_req.db', table='init_verif_req')

		


	def gen_keys(self):
		self.privkey, self.pubkey = e.create_keypair()
		print(f"priv: {self.privkey.to_ascii(encoding='hex')}")
		print(f"pub: {self.pubkey.to_ascii(encoding='hex')}")

	def gen_uniq_id(self):
		return (uuid.uuid1()).hex

	def request_join(self):
		jr = JoinRequest(
			self.username,
			self.pubUserID,
			self.request_role,
			self.pubkey.to_ascii(encoding='hex'),
			endorser1 = self.end1ID,
			endorser2 = self.end2ID,
			endorser3 = self.end3ID
			)

		jr.post_req()

if __name__ == '__main__':
	t = temp('abhi', 'student' 1111, 2222, 3333)
	t.pubUserID = 4444
	t.request_join()
