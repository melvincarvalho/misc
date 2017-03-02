import tornado.ioloop
import tornado.web
import time
import logging
import logconf
from flask import json as flask_json

logger = logging.getLogger(__name__)
_handler = logging.StreamHandler()
logger.addHandler(_handler)
logger.propagate = False

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        logger.info(self.get_arguments("model_id"))
        ss = int(self.get_argument('ss',1))
        logger.info("sleeping for %s seconds...." % (ss,))
        time.sleep(ss)
        self.write("woke up")
        logger.info('done')

    def post(self):
        logger.info("POST: (%s) %s",
                    type(self.request.arguments),
                    self.request.arguments
        )
        print "self.request.body: (%s) %s" % (
            type(self.request.body), self.request.body)
        d = tornado.escape.json_decode(self.request.body)
        logger.info("D: %s", d)
        self.write("ok")

class EmptyHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(flask_json.dumps([]))

class MockFuture(tornado.concurrent.Future):
    def __init__(self, result=None):
        super(MockFuture, self).__init__()
        self._result = result
        self.start_time = time.time()
        self._done = False

    def result(self, timeout=None):
        return self._result

def f1():
    return MockFuture(result="this is the future")

class AsyncHandler(tornado.web.RequestHandler):
    #@tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        f = yield f1()
        self.write(f)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/job/update", MainHandler),
        (r"/empty", EmptyHandler),
        (r"/async1", AsyncHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(9001)
    tornado.ioloop.IOLoop.current().start()
