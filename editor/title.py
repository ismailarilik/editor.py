class Title:
    def __init__(self, unsaved_changes_specifier, unsaved_file_name, app_name, is_there_unsaved_change=False,
        is_file_unsaved=True, file_name=None, folder_name=None):
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
            title_string += f'{self.unsaved_changes_specifier} '

        file_name = self.unsaved_file_name if self.is_file_unsaved else self.file_name
        title_string += file_name

        if self.folder_name:
            title_string += f' - {self.folder_name}'

        title_string += f' - {self.app_name}'

        return title_string
