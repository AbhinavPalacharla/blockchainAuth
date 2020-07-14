import uuid
import ed25519

class User():

	def __init__(self, uname, passwd):
		self.username = uname
		self.password = self.encrypt(passwd)
		self.pubUserID = self.gen_uniq_id()
		self.privUserID = self.gen_uniq_id()
		self.pubkey = None
		self.privkey = None

		self.gen_keys()

	def encrypt(self, passwd):
		pass #implement later, need to use external lib for encryption

	def gen_keys(self):
		self.privkey, self.pubkey = ed25519.create_keypair()
		print(f"priv: {self.privkey.to_ascii(encoding='hex')}")
		print(f"pub: {self.pubkey.to_ascii(encoding='hex')}")

	def gen_uniq_id(self):
		return (uuid.uuid1()).hex

if __name__ == '__main__':
	u = User('abhi', 'abhipasswd')
	u.gen_keys()
