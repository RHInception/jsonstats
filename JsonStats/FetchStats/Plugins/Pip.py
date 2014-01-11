import datetime
import re
from JsonStats.FetchStats import Fetcher


class Pip(Fetcher):

    def __init__(self):
        """
        Returns a list of gems available on the system.
        """
        self.context = 'pip'
        self.regex = re.compile('([A-Za-z0-9_\-]*)\s*(\([0-9\.]*\))')
        self._load_data()

    def _load_data(self):
        self._refresh_time = datetime.datetime.utcnow()
        self._packages = {}

        cmd = 'pip list'

        try:
            for line in self._exec(cmd).split('\n')[:-1]:
                package = self.regex.match(line)
                if (package is not None):
                    package_name = package.group(1)
                    package_version = package.group(2)
                    self._packages[package_name] = package_version
            self._loaded(True)
        except Exception, e:
            self._loaded(False, str(e))

    def dump(self):
        # poor mans cache, refresh cache in an hour
        if (datetime.datetime.utcnow() -
                datetime.timedelta(minutes=1)) > self._refresh_time:
            self._load_data()
        return self._packages

    def dump_json(self):
        return self.json.dumps(self.dump(), sort_keys=True, separators=(',', ': '))
