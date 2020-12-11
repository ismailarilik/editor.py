class Store:
    def __init__(self, application):
        self.application = application

        self._application_name = None
        self._has_unsaved_changes = False
        self._opened_file_name = None
        self._opened_folder_name = None

    @property
    def application_name(self):
        return self._application_name

    @application_name.setter
    def application_name(self, value):
        self._application_name = value
        self.update_title_view()

    @property
    def has_unsaved_changes(self):
        return self._has_unsaved_changes

    @has_unsaved_changes.setter
    def has_unsaved_changes(self, value):
        self._has_unsaved_changes = value
        self.update_title_view()

    @property
    def opened_file_name(self):
        return self._opened_file_name

    @opened_file_name.setter
    def opened_file_name(self, value):
        self._opened_file_name = value
        self.update_title_view()

    @property
    def opened_folder_name(self):
        return self._opened_folder_name

    @opened_folder_name.setter
    def opened_folder_name(self, value):
        self._opened_folder_name = value
        self.update_title_view()

    def update_title_view(self):
        title = ''

        if self.has_unsaved_changes:
            title += '*'
        if self.opened_file_name:
            title += f'{self.opened_file_name} - '
        if self.opened_folder_name:
            title += f'{self.opened_folder_name} - '
        if self.application_name:
            title += self.application_name

        self.application.title(title)



    def close_file_in_editor(self, file):
        self.application.editor_notebook.close_editor_by_file(file)

    def is_file_open_in_editor(self, file):
        return self.application.editor_notebook.is_file_open(file)

    def rename_file_in_editor(self, old_file, new_file):
        self.application.editor_notebook.rename_file(old_file, new_file)

    def open_file_by_file(self, file, cursor_index=None):
        self.application.editor_notebook.open_file_by_file(file, cursor_index=cursor_index)

    def get_folder(self):
        return self.application.explorer.folder

    def select_search_view(self):
        self.application.left_notebook.select(1)
