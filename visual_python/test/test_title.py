import unittest
from ..title import Title

class TestTitle(unittest.TestCase):
    def setUp(self):
        self.unsaved_changes_specifier = '*'
        self.file_name = 'file'
        self.folder_name = 'folder'
        self.separator = ' - '
        self.application_name = 'Visual Python'
        self.title = Title(self.application_name)

    def test_if_default_unsaved_changes_specifier_is_asterisk(self):
        self.assertEqual(self.title.unsaved_changes_specifier, '*')

    def test_title_string(self):
        self.assertEqual(str(self.title), self.application_name)

    def test_title_string_with_unsaved_changes(self):
        self.title.is_there_unsaved_change = True
        self.assertEqual(str(self.title), f'{self.unsaved_changes_specifier}{self.application_name}')

    def test_title_string_with_file_name(self):
        self.title.file_name = self.file_name
        self.assertEqual(str(self.title), f'{self.file_name}{self.separator}{self.application_name}')

    def test_title_string_with_folder_name(self):
        self.title.folder_name = self.folder_name
        self.assertEqual(str(self.title), f'{self.folder_name}{self.separator}{self.application_name}')

    def test_title_string_with_unsaved_changes_and_file_name_and_folder_name(self):
        self.title.is_there_unsaved_change = True
        self.title.file_name = self.file_name
        self.title.folder_name = self.folder_name
        self.assertEqual(str(self.title), f'{self.unsaved_changes_specifier}{self.file_name}{self.separator}{self.folder_name}{self.separator}{self.application_name}')
