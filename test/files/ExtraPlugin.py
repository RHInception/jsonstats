"""
Dummy plugin used for the extra_plugins test
"""

from JsonStats.FetchStats import Fetcher
class ExtraPlugin(Fetcher):
    def __init__(self):
        self.context = 'extraplugin'
        self._load_data()
    def _load_data(self):
        self._loaded(True)
    def dump(self):
        return {}
    def dump_json(self):
        return self.json.dumps(self.dump())
