from tornado import gen
from tornado.ioloop import IOLoop
import traceback

@gen.coroutine
def throw():
    10/0 # Exception here
    return 'hello'


@gen.coroutine
def test():
    while True:
        print "i'm ok"
        try:
            res = yield gen.Task(throw)
        except:
            print "caught exception"
            traceback.print_exc()
        print "here too" # it is never executed


test()
print "now starting ioloop"
IOLoop.instance().start()
