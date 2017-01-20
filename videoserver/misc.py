#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import collections

import log


def getscriptpath(script):
    return os.path.dirname(os.path.realpath(script))


def getstarterdir():
    return getscriptpath(__file__)


def getlastpathpart(path):
    return os.path.basename(os.path.normpath(path))


def islistlike(obj):
    return isinstance(obj, (list, tuple, collections.UserList))


def getmodulename(func):
    return func.__module__.split(".")[-1]


def debug(*args, sep=" "):
    log.debug(sep.join(args))
