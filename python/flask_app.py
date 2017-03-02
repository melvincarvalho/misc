import os
import sys
import time
import logging
#from logging.handlers import RotatingFileHandler
#from logging import FileHandler
#import myra.v2.logservice as logservice
import logconf
import psycopg2

from flask import Flask, request, session, render_template, jsonify, redirect, url_for, send_from_directory, jsonify

#logger = logservice.getLogger(__name__)
#logger = logservice.getLogger('')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.logger.addHandler(logconf._handler)
app.logger.setLevel(logging.DEBUG)

dbstring = "dbname='nishant_dev1' user='myraadmin' host='myra-db-dev.cihwyaszqq2o.us-west-2.rds.amazonaws.com' password='6tfc%RDX'"
conn = psycopg2.connect(dbstring)
conn.autocommit = True


@app.route("/begin", methods=["GET","POST"])
def begin():
    cur = conn.cursor()
    print >> sys.stderr, "starting transaction"
    cur.execute("begin")
    return "OK"

@app.route("/commit", methods=["GET","POST"])
def commit():
    print >> sys.stderr, "commit transaction"
    conn.commit()
    return "OK"

@app.route("/rollback", methods=["GET","POST"])
def rollback():
    print >> sys.stderr, "rollback transaction"
    conn.rollback()
    return "OK"

@app.route("/sql", methods=["GET","POST"])
def base2():
    print "/sql called"
    sql = request.form.get("sql")
    print "SQL: %s" % (sql,)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        r = cur.fetchall()
        return "%s" % (r,)
    finally:
        #conn.commit()
        print "closing cursor"
        cur.close()
        sys.stdout.flush()

@app.route("/sqlexe", methods=["GET","POST"])
def base3():
    print "/sqlexe called"
    sql = request.form.get("sql")
    print "SQL: %s" % (sql,)
    cur = conn.cursor()
    try:
        r = cur.execute(sql)
        return "%s" % (r,)
    finally:
        #conn.commit()
        print "closing cursor"
        cur.close()
        sys.stdout.flush()

@app.route("/", methods=["GET","POST"])
def base():
    print "DICT: %s" % (request.__dict__,)
    print "\nDATA: %s" % (request.data,)

    print "\n\nFORM: %s" % (request.form,)
    print "\n\nJSON: %s" % (request.get_json(silent=True),)
    #d = tornado.escape.json_decode(self.request_body)
    #logger.info("D: %s", d)
    logger.info("(%s) logging for hellow world!" % (os.getpid(),))
    time.sleep(int(request.args.get("ss",0)))
    logger.info("(%s) returning" % (os.getpid(),))
    return "(%s) hellow world!" % (os.getpid(),)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
