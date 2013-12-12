import datetime
from JsonStats.FetchStats import Fetcher
import os.path


class Facter(Fetcher):
    """
    Facter plugin for `jsonstats`. Returns key-value pairs of general
    system information provided by the `facter` command.

    Load conditions:
    * Plugin will load if the `facter` command is found

    Operating behavior:
    * Plugin will call `facter` with the `-p` (return `puppet` facts)
      option if the `puppet` command is on the system.

    Dependencies:
    * Facter - http://puppetlabs.com/blog/facter-part-1-facter-101

    Optional dependencies:
    * Puppet - http://puppetlabs.com/puppet/what-is-puppet
    """

    import yaml

    def __init__(self):
        self.context = 'facter'
        self._cmd = 'facter --yaml'

        if os.path.exists('/usr/bin/puppet'):
            self._cmd = 'facter -p --yaml'
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
