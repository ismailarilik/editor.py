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

    def test_if_first_menu_is_file_menu(self):
        first_menu_label = self.application.menu.entrycget(1, 'label')
        self.assertEqual(first_menu_label, 'File')

    def test_if_second_menu_is_edit_menu(self):
        second_menu_label = self.application.menu.entrycget(2, 'label')
        self.assertEqual(second_menu_label, 'Edit')

    def test_if_first_file_menu_command_is_open_file(self):
        first_file_menu_command_label = self.application.file_menu.entrycget(1, 'label')
        self.assertEqual(first_file_menu_command_label, 'Open File')

    def test_if_open_file_accelerator_is_ctrl_o(self):
        open_file_accelerator = self.application.file_menu.entrycget('Open File', 'accelerator')
        self.assertEqual(open_file_accelerator, 'Ctrl+O')

    def test_if_open_file_command_is_right(self):
        open_file_command = self.application.file_menu.entrycget('Open File', 'command')
        self.assertIn('open_file', open_file_command)
