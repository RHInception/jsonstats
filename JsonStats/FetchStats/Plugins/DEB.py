import datetime
from JsonStats.FetchStats import Fetcher


class DEB(Fetcher):

    def __init__(self):
        """
        Returns a deb manifest (all debs installed on the system)
        """
        self.context = 'deb'
        self._load_data()

    def _load_data(self):
        self._refresh_time = datetime.datetime.utcnow()
        self._debs = {}

        cmd = 'dpkg-query -W'

        try:
            for line in self._exec(cmd).split('\n')[:-1]:
                (deb_name, deb_version) = line.split()
                self._debs[deb_name] = deb_version
            self._loaded(True)
        except Exception, e:
            self._loaded(False, str(e))

    def dump(self):
        # poor mans cache, refresh cache in an hour
        if (datetime.datetime.utcnow() -
                datetime.timedelta(hours=1)) > self._refresh_time:
            self._load_data()
        return self._debs

    def dump_json(self):
        return self.json.dumps(self.dump())
