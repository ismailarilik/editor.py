import unittest
from .. import Application

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.application = Application()

    def test_if_application_name_is_visual_python(self):
        self.assertEqual(self.application.application_name, 'Visual Python')
