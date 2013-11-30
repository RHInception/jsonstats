import datetime
from JsonStats.FetchStats import Fetcher


class Facter(Fetcher):
    import yaml

    def __init__(self):
        self.context = 'facter'
        self._cmd = 'facter --yaml'

        try:
            import rpm
            ts = rpm.TransactionSet()
            mi = ts.dbMatch('name', 'puppet')
            if mi.count() > 0:
                self._cmd = 'facter -p --yaml'
        except:
            pass
        self._load_data()

    def _load_data(self):
        self._refresh_time = datetime.datetime.utcnow()

        try:
            output = self._exec(self._cmd)
            self.facts = self.yaml.load(output)
            self._loaded(True)
        except OSError, e:
            # Couldn't find facter command, most likely
            self._loaded(False, msg=str(e))
        except Exception, e:
            # Something else did indeed go wrong
            self._loaded(False, msg=str(e))

    def dump(self):
        # poor mans cache, refresh cache in an hour
        if (datetime.datetime.utcnow() -
                datetime.timedelta(minutes=5)) > self._refresh_time:
            self._load_data()
        return self.facts

    def dump_json(self):
        return self.json.dumps(self.dump())
