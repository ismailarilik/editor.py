import unittest
import tkinter as tk
from app import App

class TestEditorFrame(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.editor_frame = self.app.main_frame.editor_frame

    def test_get_text_method(self):
        text = 'Text'
        self.editor_frame.set_text(text)
        self.assertEqual(self.editor_frame.get_text(), 'Text')

    def test_set_text_method(self):
        text = 'Text'
        self.editor_frame.set_text(text)
        self.assertEqual(self.editor_frame.get_text(), 'Text')
