import subprocess
import sys, os
import time
import random

if __name__ == "__main__":
    rint = random.randint(100,1000)
    print "rint: %s" % (rint,)
    os.putenv("STATUS_FILE_DIR", "%s" % (rint,))
    #ret = subprocess.Popen("python worker_daemon.py 10", shell=True)
    ret = subprocess.Popen('python daemonize.py "python /Users/nishant/personal/misc/python/processes/worker2.py"', shell=True)
    #print "controller: ret: %s" % (ret.pid,)
    #time.sleep(3)
    #ret = subprocess.Popen('python daemonize.py "python /Users/nishant/personal/misc/python/processes/worker2.py"', shell=True)
    #ret = subprocess.Popen("python worker_daemon.py 10", shell=True)
    #print "controller: ret: %s" % (ret.pid,)
    print 'controller done - exiting'

