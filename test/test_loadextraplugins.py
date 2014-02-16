"""
Test for user-defined plugin locations
"""


from . import TestCase
import tempfile
from JsonStats.FetchStats import Fetcher
from JsonStats.Utils import load_extra_plugins
import shutil

class TestLoadExtraPlugins(TestCase):
    import os
    import os.path

    def setUp(self):
        # We create a directory to put our 'extra' plugin file into
        self._extra_dir = tempfile.mkdtemp('extra_plugin')
        self._extra_plugin = self.os.path.join(self._extra_dir, 'ExtraPlugin.py')

        # And again so we can test compound pathspec's
        self._extra_dir2 = tempfile.mkdtemp('extra_plugin2')
        self._extra_plugin2 = self.os.path.join(self._extra_dir2, 'ExtraPlugin2.py')

        self._extra_plugin_dirs = (self._extra_dir, self._extra_dir2)

        # Put the extra plugin2 into the temp dirs
        shutil.copy('test/files/ExtraPlugin.py', self._extra_plugin)
        shutil.copy('test/files/ExtraPlugin2.py', self._extra_plugin2)

    def test_load_extra_plugins(self):
        """
        Verify that we can load plugins from user-defined locations
        """
        loaded = load_extra_plugins(self._extra_dir)
        total_loaded = len(loaded)
        self.assertEqual(total_loaded, 1, msg="Loaded %d plugins (%s), expected 1" % (total_loaded, ', '.join(loaded)))

    def test_load_compound_path(self):
        """
        Verify that we can load plugins from a compound pathspec
        """
        compound_pathspec = "%s:%s" % self._extra_plugin_dirs
        loaded = load_extra_plugins(compound_pathspec)
        total_loaded = len(loaded)
        self.assertEqual(total_loaded, 2, msg="Loaded %d plugins (%s), expected 2" % (total_loaded, ', '.join(loaded)))

    def tearDown(self):
        # Cleanup all of our temporary files
        for d in self._extra_plugin_dirs:
            for f in self.os.listdir(d):
                ff = self.os.path.join(d, f)
                self.os.remove(ff)
            self.os.rmdir(d)
