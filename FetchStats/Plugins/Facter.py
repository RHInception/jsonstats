from FetchStats import Fetcher

class Facter(Fetcher):
    import yaml

    def __init__(self):
        self._load_data()
        self.context = 'facter'

    def _load_data(self):
        output = self._exec('facter -p --yaml')
        self.facts = self.yaml.load(output)

    def dump(self):
        return self.facts

    def dump_json(self):
        return self.json.dumps(self.dump())
