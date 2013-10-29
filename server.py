#!/usr/bin/env python

import json

import tornado.ioloop
import tornado.web


class StatsHandler(tornado.web.RequestHandler):
    """
    Gets and returns the stats.
    """

    def get(self):
        # TODO:
        # 1. load modules to run
        # 2. Execute each (as a coroutine?)
        # 3. Return the json all together
        self.write(json.dumps({'data': 'here'}))


application = tornado.web.Application([
    (r'/', StatsHandler),
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
