class Title(object):
	def __init__(self):
		self.unsaved_changes_specifier = '*'
		self.unsaved_file_name = '<unsaved_file>'
		self.file_name = self.unsaved_file_name
		self.app_name = 'Visual Python'
		self.is_there_unsaved_change = False

	def __str__(self):
		title_string = ''
		if self.is_there_unsaved_change:
			title_string += f'{self.unsaved_changes_specifier}'
		title_string += f'{self.file_name} - {self.app_name}'
		return title_string
