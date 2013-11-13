from FetchStats import Fetcher

class Facter(Fetcher):
    import yaml

    def __init__(self):
        self.context = 'facter'
        self._load_data()

    def _load_data(self):
        try:
            output = self._exec('facter -p --yaml')
            self.facts = self.yaml.load(output)
            self._loaded(True)
        except OSError, e:
            # Couldn't find facter command, most likely
            self._loaded(False, msg=str(e))
        except Exception, e:
            # Something else did indeed go wrong
            self._loaded(False, msg=str(e))

    def dump(self):
        return self.facts

    def dump_json(self):
        return self.json.dumps(self.dump())
