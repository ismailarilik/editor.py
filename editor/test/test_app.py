import unittest
from .. import App

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def tearDown(self):
        self.app.destroy()
