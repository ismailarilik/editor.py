class SettingsComponent(object):
	def __init__(self):
		self.settings = {
			'search': {
				'excluded_files': [
					'.git',
					'__pycache__'
				]
			}
		}
