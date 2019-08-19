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

    def test_if_icon_is_correct(self):
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

    def test_if_second_file_menu_command_is_open_folder(self):
        second_file_menu_command_label = self.application.file_menu.entrycget(2, 'label')
        self.assertEqual(second_file_menu_command_label, 'Open Folder')

    def test_if_open_folder_accelerator_is_ctrl_shift_o(self):
        open_folder_accelerator = self.application.file_menu.entrycget('Open Folder', 'accelerator')
        self.assertEqual(open_folder_accelerator, 'Ctrl+Shift+O')

    def test_if_open_folder_command_is_right(self):
        open_folder_command = self.application.file_menu.entrycget('Open Folder', 'command')
        self.assertIn('open_folder', open_folder_command)
    def test_if_third_file_menu_entry_is_a_separator(self):
        third_file_menu_entry_type = self.application.file_menu.type(3)
        self.assertEqual(third_file_menu_entry_type, 'separator')
