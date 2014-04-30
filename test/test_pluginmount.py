from . import TestCase

import JsonStats.FetchStats.Plugins
from JsonStats.FetchStats import Fetcher


class TestPluginMount(TestCase):

    def setUp(self):
        # Do stuff that has to happen on every test in this instance
        self.fetcher = Fetcher

        class _example_plugin(Fetcher):
            def __init__(self):
                self.context = 'testplugin'
                self._load_data()
            def _load_data(self):
                self._loaded(True)
            def dump(self):
                return {}
            def dump_json(self):
                return self.json.dumps(self.dump())

        self.example_plugin = _example_plugin

    def test_get_plugins(self):
        """
        Verify that after loading plugins we can see them attached to
        the Mount.
        """
        #example_plugin = self.example_plugin()
        plugins = self.fetcher.get_plugins()
        plugin_names = map(lambda x: str(x), plugins)
        discovered = len(plugins)
        self.assertGreaterEqual(discovered, 1, msg="Discovered %d plugins (%s), expected >=1" % (discovered, ', '.join(plugin_names)))

    def test_list_known_plugins(self):
        """
        Verify that known plugins can be listed.
        """
        listed_names = self.fetcher.list_known_plugins()
        # There should be 4 examples returned
        assert len(listed_names) == 4
