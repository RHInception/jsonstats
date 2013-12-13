try:
    import json
except:
    import simplejson as json
from JsonStats.FetchStats.Plugins import *
import JsonStats.FetchStats


######################################################################
class StatsApp(object):
    """
    Gets and returns the stats.
    """

    # load modules to run
    _plugins = [p for p in JsonStats.FetchStats.Fetcher.get_plugins() if p._state]

    def __call__(self, environ, start_response):
        result = {}

        # Execute each plugin
        for plugin in self._plugins:
            context = plugin.context
            result[context] = plugin.dump()

        # Return the json all together
        start_response("200 OK", [("Content-Type", "application/json")])
        return json.dumps(result, sort_keys=True, separators=(',', ': '))
