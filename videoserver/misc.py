#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import collections

import log


def debug(*args, sep=" ", istest=False):
    if istest:
        print(*tuple(log.str2ascii(arg) if isinstance(arg, str) else str(arg) for arg in args), sep=sep)
    else:
        log.debug(sep.join(args))


def getscriptpath(script):
    return os.path.dirname(os.path.realpath(script))


def islistlike(obj):
    return isinstance(obj, (list, tuple, collections.UserList))


def getstarterdir():
    return getscriptpath(__file__)
