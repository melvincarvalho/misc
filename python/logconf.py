import os
import logging
import logging.handlers

LOG_FORMAT = "[%(levelname)1.1s %(asctime)s %(name)s] %(message)s"
formatter = logging.Formatter(LOG_FORMAT)

# Get the root logger here.
logger = logging.getLogger(None)
logfile = os.getenv("LOGFILE", "/tmp/log")
_handler = logging.StreamHandler()
#_handler = logging.NullHandler()
#_handler = logging.handlers.WatchedFileHandler(logfile)
_handler.setFormatter(formatter)
logger.addHandler(_handler)
logger.setLevel(int(os.getenv("LOGLEVEL", logging.INFO)))
logger.debug("%s logger logging DEBUG", logger)
logger.info("%s logger logging INFO", logger)
logger.warn("%s logger logging WARN", logger)


