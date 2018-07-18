import unittest
from app import App

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def test_app_title(self):
        self.assertEqual(self.app.title(), 'Visual Python')

    def test_prefix_window_title_method(self):
        old_app_title = self.app.title()
        prefix = 'Prefix'
        self.app.prefix_window_title(prefix)
        self.assertEqual(self.app.title(), f'{prefix} - {old_app_title}')
