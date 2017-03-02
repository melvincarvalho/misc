import os
import sys
import time
import json
from functools import wraps
import traceback

import myra.v2.server.api_utils as api_utils

from flask import Flask, request, session, render_template, jsonify, redirect, url_for, send_from_directory, jsonify, Response

class MyException(Exception):
    def __init__(self, http_status=500, msg="Unexpected error"):
        self.http_status = http_status
        self.msg = msg

    def __str__(self):
        return self.msg

def test_wrapper1(fn):
    @wraps(fn)
    def df(*args, **kwargs):
        print >> sys.stderr, "test_wrapper1.df(%s)" % (locals(),)
        try:
            return fn(*args, **kwargs)
        except:
            print >> sys.stderr, "GOT EXCEPTION"
            raise
    return df

def test_wrapper2(fn):
    @wraps(fn)
    def df(*args, **kwargs):
        print >> sys.stderr, "test_wrapper2.df(%s)" % (locals(),)
        try:
            return fn(*args, **kwargs)
        except MyException as me:
            print >> sys.stderr, "swallowing MyException"
            r = Response(response=str(me), status=me.http_status)
            return r
        except Exception as e:
            print >> sys.stderr, "swallowing EXCEPTION"
            r = Response(response=str(e), status=500)
            return r
    return df

app = Flask(__name__)

@app.route("/me", methods=["GET","POST"])
#@api_utils.wrap_exceptions
@test_wrapper1
@test_wrapper2
def me():
    st = request.args.get("st", 500)
    msg = request.args.get("msg", "Unexpected Error")
    raise MyException(http_status=st, msg=msg)

@app.route("/e", methods=["GET","POST"])
#@api_utils.wrap_exceptions
@test_wrapper1
@test_wrapper2
def e():
    #st = request.args.get("st", 500)
    msg = request.args.get("msg", "Unexpected Error")
    raise Exception(msg)


@app.route("/", methods=["GET","POST"])
def base():
    print "DICT: %s" % (request.__dict__,)
    print "\nDATA: %s" % (request.data,)
    print "\n\nFORM: %s" % (request.form,)
    print "\n\nrequest.url: %s" % (request.url,)
    if request.json:
        print "\n\nrequest.json: (%s) %s" % (
            type(request.json), request.json)

    response = Response("""<h1>Gabs page.</h1> <font color="blue">This is where Gab shows what books he has been reading.</font><br><a href="/gabs_movies">Gabs movies</a>""")
    response.status_code = 200
    return response

@app.route("/rs", methods=["GET", "POST"])
def rs():
    r = request.args.get("s")
    response = Response("Returning http status: %s" % (r,))
    response.status_code = int(r)
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)
