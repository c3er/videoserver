#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import collections


def getscriptpath(script):
    return os.path.dirname(os.path.realpath(script))


def islistlike(listobj):
    return isinstance(listobj, (list, tuple, collections.UserList))


def getmodulename(func):
    return func.__module__.split(".")[-1]