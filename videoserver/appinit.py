#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask


__all__ = ["app", "initapp"]


app = None


def initapp(port):
    app.run(port=port)


if not app:
    app = flask.Flask(__name__)