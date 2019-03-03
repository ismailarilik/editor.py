import unittest
import tkinter as tk
from .. import App

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

    def tearDown(self):
        self.app.destroy()
