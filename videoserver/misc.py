#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import collections
import string

import config


def getscriptpath(script):
    return os.path.dirname(os.path.realpath(script))


def islistlike(listobj):
    return isinstance(listobj, (list, tuple, collections.UserList))


def getmodulename(func):
    return func.__module__.split(".")[-1]


def str2ascii(text):
    charlist = list(text)
    for i, char in enumerate(charlist):
        if char not in string.printable:
            charlist[i] = "&#" + str(ord(char)) + ";"
    return "".join(charlist)


def debug(*args, sep=" "):
    if config.debug:
        parts = (str2ascii(part) for part in args)
        print(*tuple(parts), sep=sep)