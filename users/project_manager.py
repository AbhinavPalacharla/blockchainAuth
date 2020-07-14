from .user import User

class ProjectManager(User):

	def __init__(self, uname, passwd):
		super().__init__(uname, passwd)
		self.rank = 2
