
import platform

from . import TestCase

from JsonStats.FetchStats import Fetcher


class TestFetcher(TestCase):

    def setUp(self):
        # Do stuff that has to happen on every test in this instance
        self.fetcher = Fetcher()

    def test_dump(self):
        """
        Verify that Fetcher.dump isn't implemented in the base class.
        """
        self.assertRaises(NotImplementedError, self.fetcher.dump)

    def test__exec(self):
        """
        Test Fetcher._exec runs a command as expected.
        """
        # Doing a directory listing should return data
        if platform.system().lower() == 'windows':
            assert self.fetcher._exec('dir')
        else:
            assert self.fetcher._exec('ls')

        # Verify cd . (which returns nothing) doens't return anything
        assert '' == self.fetcher._exec('cd .')

    def test_dump_json(self):
        """
        Test Fetch.dump_json isn't implemented in the base class.
        """
        self.assertRaises(NotImplementedError, self.fetcher.dump_json)

    def test__load_data(self):
        """
        Test Fetch._load_data isn't implemented in the base class.
        """
        self.assertRaises(NotImplementedError, self.fetcher._load_data)

    def test__loaded_true(self):
        """
        Test Fetch._loaded accurately records the 'loaded' plugin state
        """
        self.fetcher._loaded(True)
        self.assertTrue(self.fetcher._state)

    def test__loaded_false(self):
        """
        Test Fetch._loaded accurately records the 'not loaded' plugin state
        """
        self.fetcher._loaded(False, msg='test message for not loaded plugin')
        self.assertFalse(self.fetcher._state)
