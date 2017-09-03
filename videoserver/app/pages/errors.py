#!/usr/bin/env python
# -*- coding: utf-8 -*-


import traceback
import flask

import app.res


@app.web.errorhandler(500)
def internal_server_error(exc):
    return flask.render_template(
        "exception.html",
        title=app.res.INTERNAL_SERVER_ERROR_TITLE,
        message=app.res.INTERNAL_SERVER_ERROR_MSG,
        excstr=traceback.format_exc()
    ), 500


@app.web.errorhandler(IsADirectoryError)
def is_directory_error(exc):
    return flask.render_template(
        "stderror.html",
        title=app.res.ISDIRECTORY_ERROR_TITLE,
        message=app.res.ISDIRECTORY_ERROR_MSG_FORMAT.format(exc.filename)
    ), 400


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
