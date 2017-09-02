#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""This is 'my_logger' module, which is imported into all the other modules of
my application.

Based on an article in 'The Python Rag' - August 2009
"""


import sys
import string
import logging
import logging.handlers
from functools import wraps


_LOGGERNAME = "videoserver"


_logger = None
_filehandler = None
_debug_on = None


def init(logfile, debug_on=False, use_console=True):
    """Sets up the logger.
    Must be called, before any other function is called.

    Parameters:
    - logfile: Path to the logfile. If the path is not absolute, the caller has
      take care to have set the proper current diretory.
    - debug_on: If set to False (default), debug messages will be suppressed.
    """
    global _filehandler
    global _logger
    global _debug_on

    # Initialize
    _debug_on = debug_on
    _logger = logging.getLogger(_LOGGERNAME)
    _logger.setLevel(logging.DEBUG if debug_on else logging.INFO)
    
    # Setup handler
    _filehandler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1048576, backupCount=5)
    _filehandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    _logger.addHandler(_filehandler)

    # Setup log system of web framework to use the own handler
    wzlog = logging.getLogger('werkzeug')
    wzlog.setLevel(logging.INFO)
    wzlog.addHandler(_filehandler)

    if use_console:
        # Log messages shall be printed to console too
        logging.getLogger().addHandler(_ConsoleHandler(sys.stdout))

    
def close():
    """Closes the logger"""
    global _filehandler
    global _logger

    # https://stackoverflow.com/a/15474586
    handlers = _logger.handlers[:]
    for handler in handlers:
        handler.close()
        _logger.removeHandler(handler)

    if _filehandler:
        _filehandler = None
    _logger = None

    
def isready():
    """Returns whether the logger is initialized."""
    return _logger is not None and _filehandler is not None

    
def info(msg):
    """Log message with level info."""
    if isready():
        _logger.info(str(msg))

        
def debug(msg):
    """Log message with level debug."""
    if _debug_on and isready():
        _logger.debug(str(msg))

        
def error(msg):
    """Log message with level error."""
    if isready():
        _logger.error(str(msg))

        
def exception(msg):
    """Log message with level error plus exception traceback."""
    if isready():
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


def str2ascii(text):
    charlist = list(text)
    for i, char in enumerate(charlist):
        if char not in string.printable:
            charlist[i] = "&#" + str(ord(char)) + ";"
    return "".join(charlist)


class _ConsoleHandler(logging.StreamHandler):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def emit(self, record):
        record.msg = str2ascii(record.msg)
        super().emit(record)
