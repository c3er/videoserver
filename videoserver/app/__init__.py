#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask


_initialized = False


web = None
rootpath = None


def init(port, root):
    global rootpath
    rootpath = root
    web.run(port=port)


if not _initialized:
    web = flask.Flask(__name__)
    _initialized = True


import app.index