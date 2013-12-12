import datetime
from JsonStats.FetchStats import Fetcher

class Timestamp(Fetcher):
    def __init__(self):
        """
        Display the timestamp.
        """
        self.context = 'timestamp'
        self._load_data()

    def _load_data(self):
        self._timestamp = str(datetime.datetime.now())
        self._loaded(True)

    def dump(self):
        self._load_data()
        return self._timestamp

    def dump_json(self):
        return self.json.dumps(self._dump())
