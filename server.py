#!/usr/bin/env python

import json

import tornado.ioloop
import tornado.web


class StatsHandler(tornado.web.RequestHandler):
    """
    Gets and returns the stats.
    """

    def get(self):
        self.write(json.dumps({'data': 'here'}))


application = tornado.web.Application([
    (r'/', StatsHandler),
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
