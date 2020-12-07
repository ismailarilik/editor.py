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
