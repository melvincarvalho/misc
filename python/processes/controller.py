import subprocess
import sys, os
import time

if __name__ == "__main__":
    os.putenv("STATUS_FILE_DIR", "/mnt/foo/bar")
    ret = subprocess.Popen("python workers.py 10", shell=True)
    print "controller: ret: %s" % (ret.pid,)
    time.sleep(3)
    ret = subprocess.Popen("python workers.py 10", shell=True)
    print "controller: ret: %s" % (ret.pid,)
    print 'controller done - exiting'
