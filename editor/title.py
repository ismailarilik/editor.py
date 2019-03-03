class Title(object):
	def __init__(self, is_there_unsaved_change, file_name, app_name):
		self.unsaved_changes_specifier = '*'
		self.is_there_unsaved_change = is_there_unsaved_change
		self.unsaved_file_name = '<unsaved_file>'
		self.file_name = file_name if file_name else self.unsaved_file_name
		self.app_name = app_name

	def __str__(self):
		title_string = ''
		if self.is_there_unsaved_change:
			title_string += f'{self.unsaved_changes_specifier}'
		title_string += f'{self.file_name} - {self.app_name}'
		return title_string
