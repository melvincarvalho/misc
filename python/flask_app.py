import os
import sys
import time
import logging
#from logging.handlers import RotatingFileHandler
#from logging import FileHandler
#import myra.v2.logservice as logservice
#import logconf

from flask import Flask, request, session, render_template, jsonify, redirect, url_for, send_from_directory, jsonify

app = Flask(__name__)

def getRFLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        "/tmp/flask_app.log",
        maxBytes=1000,
        backupCount=100)
    logger.addHandler(handler)
    return logger

def getFLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = FileHandler("/tmp/flask_app.log")
    logger.addHandler(handler)
    return logger

#logger = getFLogger()
logger = logservice.getLogger(__name__)

@app.route("/")
def base():
    logger.info("(%s) logging for hellow world" % (os.getpid(),))
    time.sleep(int(request.args.get("ss",0)))
    logger.info("(%s) returning" % (os.getpid(),))
    return "(%s) hellow world!" % (os.getpid(),)

if __name__ == "__main__":
    #app.debug = True
    #logHandler = logging.FileHandler('/tmp/flask_app.log')
    #logHandler.setLevel(logging.INFO)
    #app.logger.addHandler(logHandler)
    #app.logger.setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=7000)
