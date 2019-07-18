class Title:
    def __init__(self, app_name, *, unsaved_changes_specifier='*', is_there_unsaved_change=False, file_name=None, folder_name=None):
        self.__app_name = app_name
        self.__unsaved_changes_specifier = unsaved_changes_specifier
        self.__is_there_unsaved_change = is_there_unsaved_change
        self.__file_name = file_name
        self.__folder_name = folder_name

    @property
    def is_there_unsaved_change(self):
        return self.__is_there_unsaved_change

    @is_there_unsaved_change.setter
    def is_there_unsaved_change(self, value):
        self.__is_there_unsaved_change = value

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, value):
        self.__file_name = value

    @property
    def folder_name(self):
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value):
        self.__folder_name = value

    def __str__(self):
        title = ''

        if self.is_there_unsaved_change:
            title += self.__unsaved_changes_specifier
        if self.file_name:
            title += f'{self.file_name} - '
        if self.folder_name:
            title += f'{self.folder_name} - '
        title += self.__app_name

        return title
