import unittest

from editor import Application

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.application = Application()
