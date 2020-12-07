import unittest

from editor.store import Store

class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = Store()

    def test_if_application_name_is_correct(self):
        self.assertEqual(self.store.application_name, 'Editor')
