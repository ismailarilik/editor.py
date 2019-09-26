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

    def test_if_first_file_menu_entry_is_a_command(self):
        first_file_menu_entry_type = self.application.file_menu.type(1)
        self.assertEqual(first_file_menu_entry_type, 'command')

    def test_if_first_file_menu_entry_label_is_open_file(self):
        first_file_menu_entry_label = self.application.file_menu.entrycget(1, 'label')
        self.assertEqual(first_file_menu_entry_label, 'Open File')

    def test_if_open_file_command_accelerator_is_ctrl_o(self):
        open_file_command_accelerator = self.application.file_menu.entrycget('Open File', 'accelerator')
        self.assertEqual(open_file_command_accelerator, 'Ctrl+O')

    def test_if_open_file_command_command_is_correct(self):
        open_file_command_command = self.application.file_menu.entrycget('Open File', 'command')
        self.assertIn('open_file', open_file_command_command)

    def test_if_second_file_menu_entry_is_a_command(self):
        second_file_menu_entry_type = self.application.file_menu.type(2)
        self.assertEqual(second_file_menu_entry_type, 'command')

    def test_if_second_file_menu_entry_label_is_open_folder(self):
        second_file_menu_entry_label = self.application.file_menu.entrycget(2, 'label')
        self.assertEqual(second_file_menu_entry_label, 'Open Folder')

    def test_if_open_folder_command_accelerator_is_ctrl_shift_o(self):
        open_folder_command_accelerator = self.application.file_menu.entrycget('Open Folder', 'accelerator')
        self.assertEqual(open_folder_command_accelerator, 'Ctrl+Shift+O')

    def test_if_open_folder_command_command_is_correct(self):
        open_folder_command_command = self.application.file_menu.entrycget('Open Folder', 'command')
        self.assertIn('open_folder', open_folder_command_command)

    def test_if_third_file_menu_entry_is_a_separator(self):
        third_file_menu_entry_type = self.application.file_menu.type(3)
        self.assertEqual(third_file_menu_entry_type, 'separator')

    def test_if_fourth_file_menu_entry_is_a_command(self):
        fourth_file_menu_entry_type = self.application.file_menu.type(4)
        self.assertEqual(fourth_file_menu_entry_type, 'command')

    def test_if_fourth_file_menu_entry_label_is_save_file(self):
        fourth_file_menu_entry_label = self.application.file_menu.entrycget(4, 'label')
        self.assertEqual(fourth_file_menu_entry_label, 'Save File')

    def test_if_save_file_command_accelerator_is_ctrl_s(self):
        save_file_command_accelerator = self.application.file_menu.entrycget('Save File', 'accelerator')
        self.assertEqual(save_file_command_accelerator, 'Ctrl+S')

    def test_if_save_file_command_command_is_correct(self):
        save_file_command_command = self.application.file_menu.entrycget('Save File', 'command')
        self.assertIn('save_file', save_file_command_command)

    def test_if_fifth_file_menu_entry_is_a_command(self):
        fifth_file_menu_entry_type = self.application.file_menu.type(5)
        self.assertEqual(fifth_file_menu_entry_type, 'command')

    def test_if_fifth_file_menu_entry_label_is_save_file_as(self):
        fifth_file_menu_entry_label = self.application.file_menu.entrycget(5, 'label')
        self.assertEqual(fifth_file_menu_entry_label, 'Save File as')

    def test_if_save_file_as_command_accelerator_is_ctrl_shift_s(self):
        save_file_as_command_accelerator = self.application.file_menu.entrycget('Save File as', 'accelerator')
        self.assertEqual(save_file_as_command_accelerator, 'Ctrl+Shift+S')

    def test_if_save_file_as_command_command_is_correct(self):
        save_file_as_command_command = self.application.file_menu.entrycget('Save File as', 'command')
        self.assertIn('save_file_as', save_file_as_command_command)

    def test_if_sixth_file_menu_entry_is_a_separator(self):
        sixth_file_menu_entry_type = self.application.file_menu.type(6)
        self.assertEqual(sixth_file_menu_entry_type, 'separator')

    def test_if_seventh_file_menu_entry_is_a_command(self):
        seventh_file_menu_entry_type = self.application.file_menu.type(7)
        self.assertEqual(seventh_file_menu_entry_type, 'command')

    def test_if_seventh_file_menu_entry_label_is_quit(self):
        seventh_file_menu_entry_label = self.application.file_menu.entrycget(7, 'label')
        self.assertEqual(seventh_file_menu_entry_label, 'Quit')

    def test_if_quit_command_accelerator_is_ctrl_q(self):
        quit_command_accelerator = self.application.file_menu.entrycget('Quit', 'accelerator')
        self.assertEqual(quit_command_accelerator, 'Ctrl+Q')

    def test_if_quit_command_command_is_correct(self):
        quit_command_command = self.application.file_menu.entrycget('Quit', 'command')
        self.assertIn('quit', quit_command_command)

    def test_if_first_edit_menu_entry_is_a_command(self):
        first_edit_menu_entry_type = self.application.edit_menu.type(1)
        self.assertEqual(first_edit_menu_entry_type, 'command')

    def test_if_first_edit_menu_entry_label_is_find_in_file(self):
        first_edit_menu_entry_label = self.application.edit_menu.entrycget(1, 'label')
        self.assertEqual(first_edit_menu_entry_label, 'Find in File')

    def test_if_find_in_file_command_accelerator_is_ctrl_f(self):
        find_in_file_command_accelerator = self.application.edit_menu.entrycget('Find in File', 'accelerator')
        self.assertEqual(find_in_file_command_accelerator, 'Ctrl+F')

    def test_if_find_in_file_command_command_is_correct(self):
        find_in_file_command_command = self.application.edit_menu.entrycget('Find in File', 'command')
        self.assertIn('find', find_in_file_command_command)

    def test_if_second_edit_menu_entry_is_a_command(self):
        second_edit_menu_entry_type = self.application.edit_menu.type(2)
        self.assertEqual(second_edit_menu_entry_type, 'command')

    def test_if_second_edit_menu_entry_label_is_search(self):
        second_edit_menu_entry_label = self.application.edit_menu.entrycget(2, 'label')
        self.assertEqual(second_edit_menu_entry_label, 'Search')

    def test_if_search_command_accelerator_is_ctrl_shift_f(self):
        search_command_accelerator = self.application.edit_menu.entrycget('Search', 'accelerator')
        self.assertEqual(search_command_accelerator, 'Ctrl+Shift+F')

    def test_if_search_command_command_is_correct(self):
        search_command_command = self.application.edit_menu.entrycget('Search', 'command')
        self.assertIn('search', search_command_command)
