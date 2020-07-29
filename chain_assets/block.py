class Block():
	def __init__(self, username, uid, pubkey, action):
		self.username = username
		self.userID = uid
		self.pubkey = pubkey #this should be a pubkey object (serialize with pickle)
		self.action = action

	def commit_to_chain(self):
		pass
