class Title:
    def __init__(self, unsaved_changes_specifier, unsaved_file_name, app_name, is_there_unsaved_change=False,
        is_file_unsaved=False, file_name='', folder_name=''):
        self.unsaved_changes_specifier = unsaved_changes_specifier
        self.unsaved_file_name = unsaved_file_name
        self.app_name = app_name

        self.is_there_unsaved_change = is_there_unsaved_change
        self.is_file_unsaved = is_file_unsaved
        self.file_name = file_name
        self.folder_name = folder_name

    def __str__(self):
        title_string = ''

        if self.is_there_unsaved_change:
            title_string += self.unsaved_changes_specifier

        if self.file_name:
            title_string += f'{self.file_name} - '
        elif self.is_file_unsaved:
            title_string += f'{self.unsaved_file_name} - '

        if self.folder_name:
            title_string += f'{self.folder_name} - '

        title_string += self.app_name

        return title_string
