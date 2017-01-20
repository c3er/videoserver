#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app.res


@app.web.errorhandler(404)
def page_not_found(exc):
    return flask.render_template(
        "stderror.html",
        title=app.res.ERROR404_TITLE,
        message=exc.description
    ), 404


@app.web.errorhandler(FileNotFoundError)
def page_not_found(exc):
    return flask.render_template(
        "stderror.html",
        title=app.res.PATHNOTFOUND_TITLE,
        message=app.res.PATHNOTFOUND_MSG_FORMAT.format(exc.filename)
    ), 404
