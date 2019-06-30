import os.path

class File:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path)
        self.extension = os.path.splitext(self.path)[1]
        self.directory_path = os.path.dirname(self.path)
        
        self.is_python_file = self.extension == '.py'