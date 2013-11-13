import datetime
from JsonStats.FetchStats import Fetcher


class RPM(Fetcher):

    def __init__(self):
        """
        Returns an rpm manifest (all rpms installed on the system.

        **Note**: This takes more than a few seconds!!
        """
        self.context = 'rpm'
        self._load_data()

    def _load_data(self, key=None):
        self._refresh_time = datetime.datetime.utcnow()
        self._rpms = {}

        # _exec will shlex.split will list-ify the cmd
        if key:
            cmd = 'rpm -q --queryformat "%%{NAME} %%{VERSION}\n" %s' % key
        else:
            cmd = 'rpm -qa --queryformat "%{NAME} %{VERSION}\n"'

        try:
            for line in self._exec(cmd).split('\n')[:-1]:
                (rpm_name, rpm_version) = line.split()
                self._rpms[rpm_name] = rpm_version
            self._loaded(True)
        except Exception, e:
            self._loaded(False, str(e))

    def dump(self, key=None):
        # poor mans cache, refresh cache in an hour
        if (datetime.datetime.utcnow() -
                datetime.timedelta(hours=1)) > self._refresh_time:
            self._load_data(key)
        return self._rpms

    def dump_json(self, key=None):
        return self.json.dumps(self.dump(key))
