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
