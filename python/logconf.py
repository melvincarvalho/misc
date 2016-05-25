import os
import logging

# Get the root logger here.
logger = logging.getLogger()
logfile = os.getenv("PY_LOGFILE", "/tmp/log")
handler = logging.FileHandler(logfile)
logger.addHandler(handler)
logger.setLevel(int(os.getenv("LOGLEVEL", logging.INFO)))
logger.debug("%s logger logging DEBUG", logger)
logger.info("%s logger logging INFO", logger)
logger.warn("%s logger logging WARN", logger)
