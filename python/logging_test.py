import os, sys
import logging
import logconf

#import myra.v2.logservice as logservice

#logger = logservice.getLogger(__name__)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("(%s) logging loglevel: %s" % (
        logger, logger.level))
    logger.debug("DEBUG")
    l2 = logging.getLogger()
    print("l2: %s" % (l2,))
    l2.setLevel(logging.DEBUG)
    logger.debug("DEBUG2")
    
