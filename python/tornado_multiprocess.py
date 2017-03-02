#!/usr/bin/env python

import random
import os
import tornado.web
from tornado.ioloop import IOLoop
from tornado import gen 
from concurrent.futures import ProcessPoolExecutor
import time
import multiprocessing

print "multiprocessing.cpu_count(): %s" % (multiprocessing.cpu_count(),)
pool = ProcessPoolExecutor(multiprocessing.cpu_count())
pool_mgr = multiprocessing.Manager()
pool_d = pool_mgr.dict()

class MyException(Exception):
    pass

def do_sleep(shared_d, sleep_secs):
    print "[%s] shared_d: %s" % (os.getpid(), shared_d)
    print "[%s] do_sleep(%s)" % (os.getpid(), locals())
    time.sleep(sleep_secs)
    print "[%s] waking up" % (os.getpid(),)
    return "slept for %s seconds" % (sleep_secs,)

def raise_exc():
    print "[%s] raising exception" % (os.getpid(),)
    raise MyException("pid=%s" % (os.getpid(),))

class AsyncHandler2(tornado.web.RequestHandler):
    #@tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        print "[%s] STARTING: %s" % (os.getpid(), self.request)
        sleep_secs = int(self.get_argument('sleep_secs', random.randint(1,10)))
        fut = pool.submit(do_sleep, pool_d, sleep_secs)
        #fut = pool.submit(raise_exc)
        print "type(fut): %s" % (type(fut),)
        try:
            ret = yield fut
        except MyException as e:
            print "caught MyException"
        self.write("[%s] async ok" % (os.getpid(),))
        #self.finish()

class AsyncHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        print "request: %s" % (self.request,)
        self.write("async ok")
        self.finish()

class AppendHandler1(tornado.web.RequestHandler):
    def get(self):
        i = int(self.get_argument('n', random.randint(0,10000)))
        pool_d[i] = i
        self.write("ok")

class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("ok")

application = tornado.web.Application([
    (r"/", DefaultHandler),
    (r"/async", AsyncHandler),
    (r"/async2", AsyncHandler2),
    (r"/append1", AppendHandler1),
    ])  

application.listen(9999)
IOLoop.instance().start()
