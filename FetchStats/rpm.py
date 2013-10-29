
import datetime

class RPM(Fetcher):

    def __init__(self):
        """
        Returns an rpm manifest (all rpms installed on the system.

        **Note**: This takes more than a few seconds!!
        """
        self._refresh_time = datetime.datetime.utcnow()
        self.load_rpm_data()

    def load_rpm_data(self):
        self._rpms = subprocess.check_output(['rpm', '-qa']).split('\n')[:-1]

    def dump_json(self, key=None):
        # poor mans cache
        if datetime.datetime.utcnow() - datetime.timedelta(hours=1) > self._refresh_time:
            self.load_rpm_data()
        return self.json.dumps(self._rpms)
