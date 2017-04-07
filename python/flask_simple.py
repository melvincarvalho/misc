import os
import sys
import time
import json
from functools import wraps
import traceback
import StringIO
import tempfile
import requests

from flask import Flask, request, session, render_template, jsonify, redirect, url_for, send_from_directory, jsonify, Response, make_response, send_file

app = Flask(__name__)

@app.route("/", defaults={"path":""}, methods=["GET","POST"])
def s1(path):
    return base(path=path)

@app.route("/api/v2/tickets.json", methods=["GET", "POST"])
def lyft_zendesk_api():
    print_request_details()
    response = Response("ok")
    response.status_code = 200
    return response

def _temp_file(url):
    f = tempfile.TemporaryFile()
    r = requests.get(url, stream=True)
    if not r.status_code in (200, 201):
        raise Exception("could not get url. status_code: %s" % (r.status_code,))
    for chunk in r.iter_content(chunk_size=100000):
        f.write(chunk)
        print >> sys.stderr, "wrote chunk (%s)" % (f.tell(),)
    f.seek(0)
    return (f, r.headers.get("Content-Type"))

def _sio_file(url):
    """Returns a file-like object that represents the contents of url,
    as well as the response itself (for examining headers etc).
    """
    f = StringIO.StringIO()
    r = requests.get(url, stream=True)
    if not r.status_code in (200, 201):
        raise Exception("could not get url. status_code: %s" % (r.status_code,))
    for chunk in r.iter_content(chunk_size=100000):
        f.write(chunk)
        print >> sys.stderr, "wrote chunk (%s)" % (f.tell(),)
    f.seek(0)
    return (f, r.headers.get("Content-Type"))

@app.route("/proxy/get", methods=["GET"])
def proxy_get():
    url = request.args.get("url")
    if not url:
        return make_response("no url found", 400)
    method = request.args.get("method", "sio")
    if method == "sio":
        (f, content_type) = _sio_file(url)
    elif method == "tempfile":
        (f, content_type) = _temp_file(url)
    print >> sys.stderr, "sending file: %s" % (f.tell(),)
    return send_file(f, mimetype=content_type)
    #return send_file('/tmp/s.jpg')
    #return Response()

@app.route("/<path:path>", methods=["GET","POST"])
def s2(path):
    return base(path=path)

def base(**kwargs):
    print_request_details(**kwargs)
    response = Response("ok")
    response.status_code = 200
    return response

def print_request_details(**kwargs):
    print "DICT: %s" % (request.__dict__,)
    print "\nDATA: %s" % (request.data,)
    print "\n\nFORM: %s" % (request.form,)
    print "\n\nrequest.url: %s" % (request.url,)
    if request.json:
        print "\n\nrequest.json: (%s) %s" % (
            type(request.json), request.json)
    print "kwargs: %s" % (kwargs,)
    
if __name__ == "__main__":
    port = 8081
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(debug=True, host="0.0.0.0", port=port)
