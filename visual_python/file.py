import os.path

class File:
    def __init__(self, path):
        self.__path = path
        self.__name = os.path.basename(self.path)
        self.__extension = os.path.splitext(self.path)[1]
        self.__directory_path = os.path.dirname(self.path)

        self.__is_python_file = self.extension == '.py'

    @property
    def path(self):
        return self.__path

    @property
    def name(self):
        return self.__name

    @property
    def extension(self):
        return self.__extension

    @property
    def directory_path(self):
        return self.__directory_path

    @property
    def is_python_file(self):
        return self.__is_python_file
