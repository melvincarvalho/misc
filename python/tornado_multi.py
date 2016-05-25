#!/usr/bin/env python

import tornado.web
from tornado.ioloop import IOLoop
from tornado import gen 
import time

import myra.v2.ml.inference_client as inference_client

@gen.coroutine
def async_sleep(seconds):
    yield gen.Task(IOLoop.instance().add_timeout, time.time() + seconds)

@gen.coroutine
def async_q(model_id):
    yield gen.Task(inference_client.get_default().predictIntent,
                   model_id, 'hello')

class InfHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        model_id = self.get_argument('model_id')
        i = yield async_q(model_id)
        print("got Intent: ", i)
        self.write("Intent: ", i)
        self.finish()

class TestHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        ss = int(self.get_argument('ss',1))
        print("sleeping for %s seconds...." % (ss,))
        for i in xrange(ss):
            print i
            yield async_sleep(1)
        self.write(str(i))
        self.finish()


application = tornado.web.Application([
    (r"/test", TestHandler),
    (r"/inf", InfHandler),
    ])  

application.listen(9999)
IOLoop.instance().start()
