
import datetime

from FetchStats import Fetcher


class RPM(Fetcher):

    def __init__(self):
        """
        Returns an rpm manifest (all rpms installed on the system.

        **Note**: This takes more than a few seconds!!
        """
        self._load_data()
        self.context = 'rpm'

    def _load_data(self, key=None):
        self._refresh_time = datetime.datetime.utcnow()
        self._rpms = {}

        # Using a full string instead of a list creates a security issue
        # when input is accepted.
        cmd = ['rpm', '-qa', '--queryformat', '"%{NAME} %{VERSION}\n"']

        if key:
            cmd.append(key)

        for line in self._exec(cmd)[1].split('\n')[:-1]:
            (rpm_name, rpm_version) = line.split()
            self._rpms[rpm_name] = rpm_version

    def dump(self, key=None):
        # poor mans cache, refresh cache in an hour
        if (datetime.datetime.utcnow() -
                datetime.timedelta(hours=1)) > self._refresh_time:
            self._load_data(key)
        return self._rpms

    def dump_json(self, key=None):
        return self.json.dumps(self.dump(key))
