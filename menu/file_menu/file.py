import os

class File(object):
	def __init__(self, path):
		self.path = path
		self.is_modified = False

	@property
	def name(self):
		if self.path:
			return os.path.basename(self.path)
