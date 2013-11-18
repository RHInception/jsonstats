from JsonStats.FetchStats.Plugins import *
import platform

from . import TestCase

import JsonStats.FetchStats.Plugins
from JsonStats.FetchStats import PluginMount
from JsonStats.FetchStats import Fetcher


class TestPluginMount(TestCase):

    def setUp(self):
        # Do stuff that has to happen on every test in this instance
        self.pluginmount = PluginMount
        self.fetcher = Fetcher

    def test_get_plugins(self):
        """
        Verify that after loading plugins we can see them attached to
        the Mount.
        """
        discovered = len(self.fetcher.get_plugins())
        expected = len(JsonStats.FetchStats.Plugins.__all__)
        self.assertEqual(discovered, expected)
