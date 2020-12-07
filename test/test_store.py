import unittest
import unittest.mock as mock

from editor import Application
from editor.store import Store

class TestStore(unittest.TestCase):
    def setUp(self):
        application = Application()
        self.store = Store(application)

    def test_if_application_name_is_correct(self):
        self.assertIsNone(self.store.application_name)

    def test_if_has_unsaved_changes_is_correct(self):
        self.assertFalse(self.store.has_unsaved_changes)

    def test_if_opened_file_name_is_correct(self):
        self.assertIsNone(self.store.opened_file_name)

    def test_if_opened_folder_name_is_correct(self):
        self.assertIsNone(self.store.opened_folder_name)

    def test_if_application_name_setter_calls_title_view_updater(self):
        self.store.update_title_view = mock.MagicMock()
        self.store.application_name = 'Editor'
        self.store.update_title_view.assert_called()

    def test_if_has_unsaved_changes_setter_calls_title_view_updater(self):
        self.store.update_title_view = mock.MagicMock()
        self.store.has_unsaved_changes = True
        self.store.update_title_view.assert_called()

    def test_if_opened_file_name_setter_calls_title_view_updater(self):
        self.store.update_title_view = mock.MagicMock()
        self.store.opened_file_name = 'a_file'
        self.store.update_title_view.assert_called()

    def test_if_opened_folder_name_setter_calls_title_view_updater(self):
        self.store.update_title_view = mock.MagicMock()
        self.store.opened_folder_name = 'a_folder'
        self.store.update_title_view.assert_called()

    def test_if_update_title_view_updates_title_with_has_unsaved_changes(self):
        self.store.has_unsaved_changes = True
        self.store.application.title = mock.MagicMock()
        self.store.update_title_view()
        self.store.application.title.assert_called_with('*')

    def test_if_update_title_view_updates_title_with_opened_file_name(self):
        self.store.opened_file_name = 'a_file'
        self.store.application.title = mock.MagicMock()
        self.store.update_title_view()
        self.store.application.title.assert_called_with('a_file - ')

    def test_if_update_title_view_updates_title_with_opened_folder_name(self):
        self.store.opened_folder_name = 'a_folder'
        self.store.application.title = mock.MagicMock()
        self.store.update_title_view()
        self.store.application.title.assert_called_with('a_folder - ')

    def test_if_update_title_view_updates_title_with_application_name(self):
        self.store.application_name = 'Editor'
        self.store.application.title = mock.MagicMock()
        self.store.update_title_view()
        self.store.application.title.assert_called_with('Editor')
