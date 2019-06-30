class Title:
    def __init__(self, app_name, unsaved_changes_specifier='*', is_there_unsaved_change=False, file_name=None, folder_name=None):
        self.app_name = app_name
        self.unsaved_changes_specifier = unsaved_changes_specifier
        self.is_there_unsaved_change = is_there_unsaved_change
        self.file_name = file_name
        self.folder_name = folder_name
    
    def __str__(self):
        title = ''
        
        if self.is_there_unsaved_change:
            title += self.unsaved_changes_specifier
        if self.file_name:
            title += f'{self.file_name} - '
        if self.folder_name:
            title += f'{self.folder_name} - '
        title += self.app_name
        
        return title