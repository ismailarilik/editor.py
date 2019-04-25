import unittest
import tkinter as tk
from .. import App
from ..title import Title

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def test_if_it_is_a_tk_instance(self):
        self.assertIsInstance(self.app, tk.Tk)

    def test_if_it_initializes_app_name_as_editor(self):
        self.assertEqual(self.app.app_name, 'Editor')

    def test_if_it_initializes_unsaved_changes_specifier_as_asterisk(self):
        self.assertEqual(self.app.unsaved_changes_specifier, '*')

    def test_if_it_initializes_unsaved_file_name_as_unsaved_file(self):
        self.assertEqual(self.app.unsaved_file_name, 'unsaved_file')

    def test_if_it_initializes_title_correctly(self):
        title = self.app._title
        self.assertIsInstance(title, Title)
        self.assertEqual(title.unsaved_changes_specifier, self.app.unsaved_changes_specifier)
        self.assertEqual(title.unsaved_file_name, self.app.unsaved_file_name)
        self.assertEqual(title.app_name, self.app.app_name)

    def test_if_it_sets_title_correctly(self):
        unsaved_file_name = self.app.unsaved_file_name
        app_name = self.app.app_name
        self.assertEqual(self.app.title(), f'{unsaved_file_name} - {app_name}')

    def test_if_it_initializes_icon_file_name_correctly(self):
        self.assertEqual(self.app.icon_file_name, 'python.png')

    def test_if_it_initializes_icon_correctly(self):
        self.assertIsInstance(self.app.icon, tk.PhotoImage)
        self.assertEqual(self.app.icon['file'], self.app.icon_file_name)

    def test_if_it_initializes_menu_correctly(self):
        self.assertIsInstance(self.app.menu, tk.Menu)

    def test_if_it_initializes_file_menu_correctly(self):
        self.assertIsInstance(self.app.file_menu, tk.Menu)
        self.assertEqual(self.app.menu.entrycget(1, 'label'), 'File')
        self.assertEqual(self.app.file_menu.entrycget(1, 'label'), 'New File')
        self.assertEqual(self.app.file_menu.entrycget(1, 'accelerator'), 'Ctrl+N')
        self.assertEqual(self.app.file_menu.entrycget(2, 'label'), 'New Folder')
        self.assertEqual(self.app.file_menu.entrycget(2, 'accelerator'), 'Ctrl+Shift+N')
        self.assertEqual(self.app.file_menu.entrycget(4, 'label'), 'Open File')
        self.assertEqual(self.app.file_menu.entrycget(4, 'accelerator'), 'Ctrl+O')
        self.assertEqual(self.app.file_menu.entrycget(5, 'label'), 'Open Folder')
        self.assertEqual(self.app.file_menu.entrycget(5, 'accelerator'), 'Ctrl+Shift+O')
        self.assertEqual(self.app.file_menu.entrycget(7, 'label'), 'Save File')
        self.assertEqual(self.app.file_menu.entrycget(7, 'accelerator'), 'Ctrl+S')
        self.assertEqual(self.app.file_menu.entrycget(8, 'label'), 'Save File as')
        self.assertEqual(self.app.file_menu.entrycget(8, 'accelerator'), 'Ctrl+Shift+S')
        self.assertEqual(self.app.file_menu.entrycget(9, 'label'), 'Save All')
        self.assertEqual(self.app.file_menu.entrycget(9, 'accelerator'), 'Ctrl+Alt+S')
        self.assertEqual(self.app.file_menu.entrycget(11, 'label'), 'Settings')
        self.assertEqual(self.app.file_menu.entrycget(11, 'accelerator'), 'Ctrl+,')
        self.assertEqual(self.app.file_menu.entrycget(13, 'label'), 'Close Editor')
        self.assertEqual(self.app.file_menu.entrycget(13, 'accelerator'), 'Ctrl+F4')
        self.assertEqual(self.app.file_menu.entrycget(14, 'label'), 'Close Folder')
        self.assertEqual(self.app.file_menu.entrycget(14, 'accelerator'), 'Ctrl+Shift+F4')
        self.assertEqual(self.app.file_menu.entrycget(16, 'label'), 'Quit')
        self.assertEqual(self.app.file_menu.entrycget(16, 'accelerator'), 'Ctrl+Q')

    def test_if_it_initializes_edit_menu_correctly(self):
        self.assertIsInstance(self.app.edit_menu, tk.Menu)
        self.assertEqual(self.app.menu.entrycget(2, 'label'), 'Edit')
        self.assertEqual(self.app.edit_menu.entrycget(1, 'label'), 'Undo')
        self.assertEqual(self.app.edit_menu.entrycget(1, 'accelerator'), 'Ctrl+Z')
        self.assertEqual(self.app.edit_menu.entrycget(2, 'label'), 'Redo')
        self.assertEqual(self.app.edit_menu.entrycget(2, 'accelerator'), 'Ctrl+Shift+Z')
        self.assertEqual(self.app.edit_menu.entrycget(4, 'label'), 'Select All')
        self.assertEqual(self.app.edit_menu.entrycget(4, 'accelerator'), 'Ctrl+A')
        self.assertEqual(self.app.edit_menu.entrycget(6, 'label'), 'Cut')
        self.assertEqual(self.app.edit_menu.entrycget(6, 'accelerator'), 'Ctrl+X')
        self.assertEqual(self.app.edit_menu.entrycget(7, 'label'), 'Copy')
        self.assertEqual(self.app.edit_menu.entrycget(7, 'accelerator'), 'Ctrl+C')
        self.assertEqual(self.app.edit_menu.entrycget(8, 'label'), 'Paste')
        self.assertEqual(self.app.edit_menu.entrycget(8, 'accelerator'), 'Ctrl+V')
        self.assertEqual(self.app.edit_menu.entrycget(10, 'label'), 'Find')
        self.assertEqual(self.app.edit_menu.entrycget(10, 'accelerator'), 'Ctrl+F')
        self.assertEqual(self.app.edit_menu.entrycget(11, 'label'), 'Replace')
        self.assertEqual(self.app.edit_menu.entrycget(11, 'accelerator'), 'Ctrl+R')
        self.assertEqual(self.app.edit_menu.entrycget(13, 'label'), 'Find in Files')
        self.assertEqual(self.app.edit_menu.entrycget(13, 'accelerator'), 'Ctrl+Shift+F')
        self.assertEqual(self.app.edit_menu.entrycget(14, 'label'), 'Replace in Files')
        self.assertEqual(self.app.edit_menu.entrycget(14, 'accelerator'), 'Ctrl+Shift+R')

    def test_if_it_initializes_view_menu_correctly(self):
        self.assertIsInstance(self.app.view_menu, tk.Menu)
        self.assertEqual(self.app.menu.entrycget(3, 'label'), 'View')
        self.assertEqual(self.app.view_menu.entrycget(1, 'label'), 'Explorer')
        self.assertEqual(self.app.view_menu.entrycget(1, 'accelerator'), 'Ctrl+Shift+E')
        self.assertEqual(self.app.view_menu.entrycget(2, 'label'), 'Search')
        self.assertEqual(self.app.view_menu.entrycget(2, 'accelerator'), 'Ctrl+Shift+F')
        self.assertEqual(self.app.view_menu.entrycget(3, 'label'), 'Version Control')
        self.assertEqual(self.app.view_menu.entrycget(3, 'accelerator'), 'Ctrl+Shift+V')
        self.assertEqual(self.app.view_menu.entrycget(4, 'label'), 'Debug')
        self.assertEqual(self.app.view_menu.entrycget(4, 'accelerator'), 'Ctrl+Shift+D')
        self.assertEqual(self.app.view_menu.entrycget(5, 'label'), 'Extensions')
        self.assertEqual(self.app.view_menu.entrycget(5, 'accelerator'), 'Ctrl+Shift+X')
        self.assertEqual(self.app.view_menu.entrycget(7, 'label'), 'Problems')
        self.assertEqual(self.app.view_menu.entrycget(7, 'accelerator'), 'Ctrl+Shift+P')
        self.assertEqual(self.app.view_menu.entrycget(8, 'label'), 'Output')
        self.assertEqual(self.app.view_menu.entrycget(8, 'accelerator'), 'Ctrl+Shift+U')
        self.assertEqual(self.app.view_menu.entrycget(9, 'label'), 'Debug Console')
        self.assertEqual(self.app.view_menu.entrycget(9, 'accelerator'), 'Ctrl+Shift+C')
        self.assertEqual(self.app.view_menu.entrycget(10, 'label'), 'Terminal')
        self.assertEqual(self.app.view_menu.entrycget(10, 'accelerator'), 'Ctrl+Shift+T')

    def test_if_it_initializes_go_menu_correctly(self):
        self.assertIsInstance(self.app.go_menu, tk.Menu)
        self.assertEqual(self.app.menu.entrycget(4, 'label'), 'Go')
        self.assertEqual(self.app.go_menu.entrycget(1, 'label'), 'Next Editor')
        self.assertEqual(self.app.go_menu.entrycget(1, 'accelerator'), 'Ctrl+PageDown')
        self.assertEqual(self.app.go_menu.entrycget(2, 'label'), 'Previous Editor')
        self.assertEqual(self.app.go_menu.entrycget(2, 'accelerator'), 'Ctrl+PageUp')
        self.assertEqual(self.app.go_menu.entrycget(4, 'label'), 'Go to File')
        self.assertEqual(self.app.go_menu.entrycget(4, 'accelerator'), 'Ctrl+P')
        self.assertEqual(self.app.go_menu.entrycget(6, 'label'), 'Go to Declaration')
        self.assertEqual(self.app.go_menu.entrycget(6, 'accelerator'), 'Ctrl+D')
        self.assertEqual(self.app.go_menu.entrycget(8, 'label'), 'Go to Line/Column')
        self.assertEqual(self.app.go_menu.entrycget(8, 'accelerator'), 'Ctrl+G')

    def test_if_it_initializes_debug_menu_correctly(self):
        self.assertIsInstance(self.app.debug_menu, tk.Menu)
        self.assertEqual(self.app.menu.entrycget(5, 'label'), 'Debug')
        self.assertEqual(self.app.debug_menu.entrycget(1, 'label'), 'Start Debugging')
        self.assertEqual(self.app.debug_menu.entrycget(1, 'accelerator'), 'F5')
        self.assertEqual(self.app.debug_menu.entrycget(2, 'label'), 'Start without Debugging')
        self.assertEqual(self.app.debug_menu.entrycget(2, 'accelerator'), 'Ctrl+F5')
        self.assertEqual(self.app.debug_menu.entrycget(3, 'label'), 'Stop Debugging')
        self.assertEqual(self.app.debug_menu.entrycget(3, 'accelerator'), 'Shift+F5')
        self.assertEqual(self.app.debug_menu.entrycget(4, 'label'), 'Restart Debugging')
        self.assertEqual(self.app.debug_menu.entrycget(4, 'accelerator'), 'Ctrl+Shift+F5')
        self.assertEqual(self.app.debug_menu.entrycget(6, 'label'), 'Step Over')
        self.assertEqual(self.app.debug_menu.entrycget(6, 'accelerator'), 'F10')
        self.assertEqual(self.app.debug_menu.entrycget(7, 'label'), 'Step Into')
        self.assertEqual(self.app.debug_menu.entrycget(7, 'accelerator'), 'F11')
        self.assertEqual(self.app.debug_menu.entrycget(8, 'label'), 'Step Out')
        self.assertEqual(self.app.debug_menu.entrycget(8, 'accelerator'), 'Shift+F11')
        self.assertEqual(self.app.debug_menu.entrycget(9, 'label'), 'Continue')
        self.assertEqual(self.app.debug_menu.entrycget(9, 'accelerator'), 'F5')
        self.assertEqual(self.app.debug_menu.entrycget(11, 'label'), 'Toggle Breakpoint')
        self.assertEqual(self.app.debug_menu.entrycget(11, 'accelerator'), 'F9')
        self.assertEqual(self.app.debug_menu.entrycget(13, 'label'), 'Enable All Breakpoints')
        self.assertEqual(self.app.debug_menu.entrycget(14, 'label'), 'Disable All Breakpoints')
        self.assertEqual(self.app.debug_menu.entrycget(15, 'label'), 'Remove All Breakpoints')

    def test_if_it_initializes_help_menu_correctly(self):
        self.assertIsInstance(self.app.help_menu, tk.Menu)
        self.assertEqual(self.app.menu.entrycget(6, 'label'), 'Help')
        self.assertEqual(self.app.help_menu.entrycget(1, 'label'), 'Report Issue')
        self.assertEqual(self.app.help_menu.entrycget(3, 'label'), 'View License')
        self.assertEqual(self.app.help_menu.entrycget(5, 'label'), 'Check for Updates')
        self.assertEqual(self.app.help_menu.entrycget(7, 'label'), 'About')

    def tearDown(self):
        self.app.destroy()

class TestSetTitleMethod(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def test_if_it_sets_title_properties_correctly(self):
        # Reset title properties
        self.app._title.is_there_unsaved_change = False
        self.app._title.is_file_unsaved = False
        self.app._title.file_name = 'file'
        self.app._title.folder_name = 'folder'
        # Call set_title method
        file_name = 'file2'
        folder_name = 'folder2'
        self.app.set_title(is_there_unsaved_change=True, is_file_unsaved=True, file_name=file_name,
            folder_name=folder_name)
        # Check title properties
        self.assertTrue(self.app._title.is_there_unsaved_change)
        self.assertTrue(self.app._title.is_file_unsaved)
        self.assertEqual(self.app._title.file_name, file_name)
        self.assertEqual(self.app._title.folder_name, folder_name)

    def test_if_it_does_not_set_title_properties_when_it_was_called_with_no_argument(self):
        # Reset title properties
        file_name = 'file'
        folder_name = 'folder'
        self.app._title.is_there_unsaved_change = False
        self.app._title.is_file_unsaved = False
        self.app._title.file_name = file_name
        self.app._title.folder_name = folder_name
        # Call set_title method with no argument
        self.app.set_title()
        # Check title properties
        self.assertFalse(self.app._title.is_there_unsaved_change)
        self.assertFalse(self.app._title.is_file_unsaved)
        self.assertEqual(self.app._title.file_name, file_name)
        self.assertEqual(self.app._title.folder_name, folder_name)

    def test_if_it_sets_app_title_to_title_string_value(self):
        # Reset title properties
        file_name = 'file'
        folder_name = 'folder'
        self.app._title.is_there_unsaved_change = False
        self.app._title.is_file_unsaved = False
        self.app._title.file_name = file_name
        self.app._title.folder_name = folder_name
        # Call set_title method
        self.app.set_title()
        # Check app title
        self.assertEqual(self.app.title(), str(self.app._title))

    def tearDown(self):
        self.app.destroy()
