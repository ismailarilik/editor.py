class Title:
    def __init__(self, application_name, unsaved_changes_specifier='*', is_there_unsaved_change=False, file_name=None, folder_name=None, separator=' - '):
        self.__application_name = application_name
        self.__unsaved_changes_specifier = unsaved_changes_specifier
        self.__is_there_unsaved_change = is_there_unsaved_change
        self.__file_name = file_name
        self.__folder_name = folder_name
        self.__separator = separator

    @property
    def unsaved_changes_specifier(self):
        return self.__unsaved_changes_specifier

    @property
    def is_there_unsaved_change(self):
        return self.__is_there_unsaved_change

    @is_there_unsaved_change.setter
    def is_there_unsaved_change(self, is_there_unsaved_change):
        self.__is_there_unsaved_change = is_there_unsaved_change

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, file_name):
        self.__file_name = file_name

    @property
    def folder_name(self):
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, folder_name):
        self.__folder_name = folder_name

    @property
    def separator(self):
        return self.__separator

    def __str__(self):
        title = ''

        if self.is_there_unsaved_change:
            title += self.unsaved_changes_specifier
        if self.file_name:
            title += f'{self.file_name}{self.separator}'
        if self.folder_name:
            title += f'{self.folder_name}{self.separator}'
        title += self.__application_name

        return title
