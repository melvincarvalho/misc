import os
import sys
import time
import logging
#from logging.handlers import RotatingFileHandler
#from logging import FileHandler
#import myra.v2.logservice as logservice
import logconf

from flask import Flask, request, session, render_template, jsonify, redirect, url_for, send_from_directory, jsonify

#logger = logservice.getLogger(__name__)
#logger = logservice.getLogger('')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.logger.addHandler(logconf._handler)
app.logger.setLevel(logging.DEBUG)

@app.route("/")
def base():
    logger.info("(%s) logging for hellow world" % (os.getpid(),))
    time.sleep(int(request.args.get("ss",0)))
    logger.info("(%s) returning" % (os.getpid(),))
    return "(%s) hellow world!" % (os.getpid(),)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
