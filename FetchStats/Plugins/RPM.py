
import datetime

from FetchStats import Fetcher

"""
TODO:

- Turn the newline split list into a dictionary

- Make dump_json use the key parameter to return just a specific RPM
  version
"""



class RPM(Fetcher):

    def __init__(self):
        """
        Returns an rpm manifest (all rpms installed on the system.

        **Note**: This takes more than a few seconds!!
        """
        self._load_data()
        self.plugin_name = 'rpm'

    def _load_data(self):
        self._refresh_time = datetime.datetime.utcnow()
        self._rpms = self._exec(['rpm', '-qa'])[1].split('\n')[:-1]

    def dump(self):
        # poor mans cache, refresh cache in an hour
        if datetime.datetime.utcnow() - datetime.timedelta(hours=1) > self._refresh_time:
            self._load_data()
        return self._rpms

    def dump_json(self):
        return self.json.dumps(self.dump())
