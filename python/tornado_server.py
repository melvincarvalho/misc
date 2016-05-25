import tornado.ioloop
import tornado.web
import time
import logging
import logconf

logger = logging.getLogger(__name__)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        ss = int(self.get_argument('ss',1))
        logger.info("sleeping for %s seconds...." % (ss,))
        time.sleep(ss)
        self.write("woke up")
        logger.info('done')

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
