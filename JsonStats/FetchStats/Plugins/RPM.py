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

    def _load_data(self):
        self._refresh_time = datetime.datetime.utcnow()
        self._rpms = {}

        cmd = 'rpm -qa --queryformat "%{NAME} %{VERSION}-%{RELEASE}.%{ARCH}\n"'

        try:
            for line in self._exec(cmd).split('\n')[:-1]:
                (rpm_name, rpm_version) = line.split()
                self._rpms[rpm_name] = rpm_version
            self._loaded(True)
        except Exception, e:
            self._loaded(False, str(e))

    def dump(self):
        # poor mans cache, refresh cache in an hour
        if (datetime.datetime.utcnow() -
                datetime.timedelta(minutes=1)) > self._refresh_time:
            self._load_data()
        return self._rpms

    def dump_json(self):
        return self.json.dumps(self.dump())
