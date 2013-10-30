#!/usr/bin/env python

import json

import tornado.ioloop
import tornado.web

from FetchStats.Plugins import *
import FetchStats

class StatsHandler(tornado.web.RequestHandler):
    """
    Gets and returns the stats.
    """


    _plugins = FetchStats.Fetcher.get_plugins()

    def get(self):
        result = {}
        # 1. load modules to run
        #     - handled in the '... Plugins import *' line

        # 2. Execute each (as a coroutine?)
        #     - currently handled during instantiation

        for plugin in self._plugins:
            context = plugin.context
            result[context] = plugin.dump()
        # 3. Return the json all together
        self.write(json.dumps(result))


application = tornado.web.Application([
    (r'/', StatsHandler),
])


if __name__ == "__main__":
    print "plugins loaded..."
    print "server listening on http://0.0.0.0:8888"
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
