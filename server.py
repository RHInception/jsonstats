#!/usr/bin/env python

try:
    import json
except:
    import simplejson as json

from FetchStats.Plugins import *

import FetchStats

# TODO: logging!


class StatsApp(object):
    """
    Gets and returns the stats.
    """

    # load modules to run
    _plugins = FetchStats.Fetcher.get_plugins()

    def __call__(self, environ, start_response):
        result = {}

        # Execute each plugin
        for plugin in self._plugins:
            context = plugin.context
            result[context] = plugin.dump()

        # Return the json all together
        start_response("200 OK", [("Content-Type", "application/json")])
        return json.dumps(result)


if __name__ == "__main__":
    print "plugins loaded..."
    print "server listening on http://0.0.0.0:8888"
    try:
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8888, StatsApp())
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "shutting down..."
        raise SystemExit(0)
