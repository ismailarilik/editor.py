import unittest
from ..title import Title

class TestTitle(unittest.TestCase):
    def setUp(self):
        self.title = Title(unsaved_changes_specifier='*', unsaved_file_name='unsaved_file', app_name='Editor')

    def test_if_it_sets_is_there_unsaved_change_property_as_false(self):
        self.assertFalse(self.title.is_there_unsaved_change)

    def test_if_it_sets_is_file_unsaved_property_as_true(self):
        self.assertTrue(self.title.is_file_unsaved)

    def test_if_it_sets_file_name_property_as_none(self):
        self.assertIsNone(self.title.file_name)

    def test_if_it_sets_folder_name_property_as_none(self):
        self.assertIsNone(self.title.folder_name)

class TestStrMethod(unittest.TestCase):
    def setUp(self):
        self.unsaved_changes_specifier = '*'
        self.unsaved_file_name = 'unsaved_file'
        self.app_name = 'Editor'
        self.title = Title(unsaved_changes_specifier=self.unsaved_changes_specifier,
            unsaved_file_name=self.unsaved_file_name, app_name=self.app_name)

    def test_if_it_returns_title_string_correctly(self):
        # Reset title properties
        file_name = 'file'
        folder_name = 'folder'
        self.title.is_there_unsaved_change = True
        self.title.is_file_unsaved = False
        self.title.file_name = file_name
        self.title.folder_name = folder_name
        # Check return value
        title = f'{self.unsaved_changes_specifier} {file_name} - {folder_name} - {self.app_name}'
        self.assertEqual(str(self.title), title)

    def test_if_it_adds_unsaved_changes_specifier_to_return_value_if_is_there_unsaved_change_property_is_true(self):
        self.title.is_there_unsaved_change = True
        self.assertTrue(str(self.title).startswith('*'))

    def test_if_it_adds_unsaved_file_name_to_return_value_if_is_file_unsaved_property_is_true(self):
        self.title.is_file_unsaved = True
        self.assertIn(self.unsaved_file_name, str(self.title))

    def test_if_it_adds_file_name_to_return_value_if_is_file_unsaved_property_is_false(self):
        file_name = 'file'
        self.title.is_file_unsaved = False
        self.title.file_name = file_name
        self.assertIn(file_name, str(self.title))

    def test_if_it_adds_folder_name_to_return_value_if_folder_name_property_is_not_none(self):
        folder_name = 'folder'
        self.title.folder_name = folder_name
        self.assertIn(folder_name, str(self.title))

    def test_if_it_adds_app_name_to_return_value(self):
        self.assertIn(self.app_name, str(self.title))
