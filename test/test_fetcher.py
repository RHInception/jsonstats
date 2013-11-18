
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