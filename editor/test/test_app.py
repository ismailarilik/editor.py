import unittest
import tkinter as tk
from .. import App

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def test_if_it_is_a_tk_instance(self):
        self.assertIsInstance(self.app, tk.Tk)

    def tearDown(self):
        self.app.destroy()
