import time
import sys, os
import signal
import daemon
import logging
import time

with daemon.DaemonContext():
    main()

logger = logging.getLogger()
handler = logging.FileHandler("/tmp/workers.log")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def sigint_handler(signal, frame):
    logger.info('[%s] sigint_handler called' % (os.getpid(),))

signal.signal(signal.SIGINT, sigint_handler)

def main():
    pids = 'pid: %s, ppid: %s, exe: %s' % (
        os.getpid(), os.getppid(), sys.executable)
    logger.info('[%s] started. env_var: %s' % (pids, os.getenv("STATUS_FILE_DIR")))
    sleep_time = 10
    if len(sys.argv) > 1:
        sleep_time = int(sys.argv[1])
    logger.info('[%s] sleeping %s seconds' % (pids, sleep_time))
    f = open('/tmp/worker_daemon.out', 'a')
    print >> f, "[%s, %s] is alive" % (os.getpid(), time.time())
    f.flush()
    time.sleep(sleep_time)
    print >> f, "[%s, %s] is alive" % (os.getpid(), time.time())
    f.close()
    logger.info('[%s] woke up. done.' % (pids,))

