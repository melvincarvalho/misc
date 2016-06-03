import time
import sys, os

if __name__ == "__main__":
    pids = 'pid: %s, ppid: %s, exe: %s' % (
        os.getpid(), os.getppid(), sys.executable)
    print '[%s] started. env_var: %s' % (pids, os.getenv("STATUS_FILE_DIR"))
    sleep_time = 10
    if len(sys.argv) > 1:
        sleep_time = int(sys.argv[1])
    print '[%s] sleeping %s seconds' % (pids, sleep_time)
    time.sleep(sleep_time)
    print '[%s] woke up. done.' % (pids,)

