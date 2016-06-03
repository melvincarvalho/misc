import os, sys
import logging
#import logconf

#import myra.v2.logservice as logservice

#logger = logservice.getLogger(__name__)
#logger = logging.getLogger(__name__)

def main1():
    logger.info("(%s) logging loglevel: %s" % (
        logger, logger.level))
    logger.debug("DEBUG")
    l2 = logging.getLogger('')
    print("l2: %s" % (l2,))
    logger.setLevel(logging.DEBUG)
    logger.debug("DEBUG2")
    l2.info("l2 info")
    l2.debug("l2 debug")

def log2():
    handler = logging.FileHandler(logconf.logfile)
    logger.addHandler(handler)
    logger.info("logging after adding handler")

def main3():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info("testing")
    
if __name__ == "__main__":
    #main1()
    #log2()
    main3()
