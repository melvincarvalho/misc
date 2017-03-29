import os
import sys
import time
import json
from functools import wraps
import traceback

from flask import Flask, request, session, render_template, jsonify, redirect, url_for, send_from_directory, jsonify, Response

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def s1():
    return base()

@app.route("/<p1>", methods=["GET","POST"])
def s2(p1):
    return base(p1=p1)

def base(**kwargs):
    print "DICT: %s" % (request.__dict__,)
    print "\nDATA: %s" % (request.data,)
    print "\n\nFORM: %s" % (request.form,)
    print "\n\nrequest.url: %s" % (request.url,)
    if request.json:
        print "\n\nrequest.json: (%s) %s" % (
            type(request.json), request.json)
    response = Response("ok")
    response.status_code = 200
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)
