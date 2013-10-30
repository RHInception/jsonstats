#import FetchStats.Fetcher
from FetchStats import Fetcher

"""
TODO:

don't just "raise wtf are you doing"
"""


class Facter(Fetcher):
    import yaml

    def __init__(self):
        self._load_data()


    def _load_data(self):
        (ret, output) = self._exec(['facter', ' -p', ' --yaml'])
        self.facts = self.yaml.load(output)

    def dump_json(self, key=None):
        if not key:
            return self.json.dumps(self.facts)
        elif key in self.result:
            return self.json.dumps(self.facts[key])
        else:
            raise "wtf are you doing"
