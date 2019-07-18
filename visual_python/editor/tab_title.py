class TabTitle:
    def __init__(self, file_name, unsaved_changes_specifier='*', is_there_unsaved_change=False):
        self.file_name = file_name
        self.unsaved_changes_specifier = unsaved_changes_specifier
        self.is_there_unsaved_change = is_there_unsaved_change
    
    def __str__(self):
        tab_title = ''
        
        if self.is_there_unsaved_change:
            tab_title += self.unsaved_changes_specifier
        tab_title += self.file_name
        
        return tab_title
