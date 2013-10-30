from FetchStats import Fetcher

"""
TODO:

don't just "raise wtf are you doing"
"""


class Facter(Fetcher):
    import yaml

    def __init__(self):
        self._load_data()
        self.plugin_name = 'facter'

    def _load_data(self):
        (ret, output) = self._exec(['facter', ' -p', ' --yaml'])
        self.facts = self.yaml.load(output)

    def dump(self):
        return self.facts

    def dump_json(self):
        return self.json.dumps(self.dump())
