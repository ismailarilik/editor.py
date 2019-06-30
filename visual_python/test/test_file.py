import unittest
from ..file import File

class TestFile(unittest.TestCase):
    def setUp(self):
        self.directory_path = '/home/user/dev'
        self.extension = '.py'
        self.name = f'code{self.extension}'
        self.path = f'{self.directory_path}/{self.name}'
        self.file = File(self.path)
    
    def test_name_property(self):
        self.assertEqual(self.file.name, self.name)
    
    def test_extension_property(self):
        self.assertEqual(self.file.extension, self.extension)
    
    def test_directory_path_property(self):
        self.assertEqual(self.file.directory_path, self.directory_path)
    
    def test_is_python_file_property(self):
        self.assertEqual(self.file.is_python_file, self.extension == '.py')