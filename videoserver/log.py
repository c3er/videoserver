#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""This is 'my_logger' module, which is imported into all the other modules of
my application.

Copied from 'The Python Rag' - August 2009
"""


import sys
import string
import logging
import logging.handlers
from functools import wraps


_LOGGERNAME = "videoserver"


_logger = None
_handler = None
_debug_on = None


def init(logfile, debug_on=False):
    """Sets up the logger.
    Must be called, before any other function is called.
    """
    global _handler
    global _logger
    global _debug_on

    # Initialize
    _debug_on = debug_on
    _logger = logging.getLogger(_LOGGERNAME)
    _logger.setLevel(logging.DEBUG if debug_on else logging.INFO)
    
    # Setup handler
    _handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1048576, backupCount=5)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    _handler.setFormatter(formatter)
    _logger.addHandler(_handler)

    # Setup log system of web framework to use the own handler
    wzlog = logging.getLogger('werkzeug')
    wzlog.setLevel(logging.INFO)
    wzlog.addHandler(_handler)

    # Log messages shall be printed to console too
    logging.getLogger().addHandler(_ConsoleHandler(sys.stdout))

    
def close():
    """Closes the logger"""
    global _handler
    global _logger
    _handler.close()
    _logger = None

    
def isready():
    """Returns the status of the logger."""
    return _logger is not None

    
def info(msg):
    """Log message with level info."""
    if _logger:
        _logger.info(str(msg))

        
def debug(msg):
    """Log message with level debug."""
    if _debug_on and _logger:
        _logger.debug(str(msg))

        
def error(msg):
    """Log message with level error."""
    if _logger:
        _logger.error(str(msg))

        
def exception(msg):
    """Log message with level error plus exception traceback."""
    if _logger:
        _logger.exception(str(msg))

        
def logfunction(f):
    """Creates a decorator to log a function."""
    @wraps(f)
    def wrapper(*args, **kw):
        debug("{} called".format(f.__name__))
        return f(*args, **kw)
    return wrapper

    
def logmethod(m):
    """Creates a decorator to log a method."""
    @wraps(m)
    def wrapper(self, *args, **kw):
        debug("{} in {} called".format(m.__name__, self.__class__.__name__))
        return m(self, *args, **kw)
    return wrapper


class _ConsoleHandler(logging.StreamHandler):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def emit(self, record):
        record.msg = self._str2ascii(record.msg)
        super().emit(record)

    @staticmethod
    def _str2ascii(text):
        charlist = list(text)
        for i, char in enumerate(charlist):
            if char not in string.printable:
                charlist[i] = "&#" + str(ord(char)) + ";"
        return "".join(charlist)
