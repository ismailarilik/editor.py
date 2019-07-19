import unittest
from .. import Application

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.application = Application()
        self.application_name = 'Visual Python'

    def tearDown(self):
        self.application.destroy()

    def test_if_application_name_is_visual_python(self):
        self.assertEqual(self.application.application_name, 'Visual Python')

    def test_if_application_initializes_title_properly(self):
        self.assertEqual(self.application.title(), self.application_name)

    def test_if_icon_is_right(self):
        self.assertIn('icons/python.png', self.application.icon['file'])
