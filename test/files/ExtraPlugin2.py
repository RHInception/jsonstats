"""
Dummy plugin #2 used for the extra_plugins compound-path test
"""

from JsonStats.FetchStats import Fetcher
class ExtraPlugin2(Fetcher):
    def __init__(self):
        self.context = 'extraplugin2'
        self._load_data()
    def _load_data(self):
        self._loaded(True)
    def dump(self):
        return {}
    def dump_json(self):
        return self.json.dumps(self.dump())
