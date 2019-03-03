import unittest
import tkinter as tk
from .. import App
from ..title import Title

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def test_if_it_is_a_tk_instance(self):
        self.assertIsInstance(self.app, tk.Tk)

    def test_if_it_initializes_app_name_as_editor(self):
        self.assertEqual(self.app.app_name, 'Editor')

    def test_if_it_initializes_unsaved_changes_specifier_as_asterisk(self):
        self.assertEqual(self.app.unsaved_changes_specifier, '*')

    def test_if_it_initializes_unsaved_file_name_as_unsaved_file(self):
        self.assertEqual(self.app.unsaved_file_name, 'unsaved_file')

    def test_if_it_initializes_title_correctly(self):
        title = self.app._title
        self.assertIsInstance(title, Title)
        self.assertEqual(title.unsaved_changes_specifier, self.app.unsaved_changes_specifier)
        self.assertEqual(title.unsaved_file_name, self.app.unsaved_file_name)
        self.assertEqual(title.app_name, self.app.app_name)

    def test_if_it_sets_title_correctly(self):
        unsaved_file_name = self.app.unsaved_file_name
        app_name = self.app.app_name
        self.assertEqual(self.app.title(), f'{unsaved_file_name} - {app_name}')

    def tearDown(self):
        self.app.destroy()

class TestSetTitleMethod(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def test_if_it_sets_title_properties_correctly(self):
        # Reset title properties
        self.app._title.is_there_unsaved_change = False
        self.app._title.is_file_unsaved = False
        self.app._title.file_name = 'file'
        self.app._title.folder_name = 'folder'
        # Call set_title method
        file_name = 'file2'
        folder_name = 'folder2'
        self.app.set_title(is_there_unsaved_change=True, is_file_unsaved=True, file_name=file_name,
            folder_name=folder_name)
        # Check title properties
        self.assertTrue(self.app._title.is_there_unsaved_change)
        self.assertTrue(self.app._title.is_file_unsaved)
        self.assertEqual(self.app._title.file_name, file_name)
        self.assertEqual(self.app._title.folder_name, folder_name)

    def test_if_it_does_not_set_title_properties_when_it_was_called_with_no_argument(self):
        # Reset title properties
        file_name = 'file'
        folder_name = 'folder'
        self.app._title.is_there_unsaved_change = False
        self.app._title.is_file_unsaved = False
        self.app._title.file_name = file_name
        self.app._title.folder_name = folder_name
        # Call set_title method with no argument
        self.app.set_title()
        # Check title properties
        self.assertFalse(self.app._title.is_there_unsaved_change)
        self.assertFalse(self.app._title.is_file_unsaved)
        self.assertEqual(self.app._title.file_name, file_name)
        self.assertEqual(self.app._title.folder_name, folder_name)

    def test_if_it_sets_app_title_to_title_string_value(self):
        # Reset title properties
        file_name = 'file'
        folder_name = 'folder'
        self.app._title.is_there_unsaved_change = False
        self.app._title.is_file_unsaved = False
        self.app._title.file_name = file_name
        self.app._title.folder_name = folder_name
        # Call set_title method
        self.app.set_title()
        # Check app title
        self.assertEqual(self.app.title(), str(self.app._title))

    def tearDown(self):
        self.app.destroy()
