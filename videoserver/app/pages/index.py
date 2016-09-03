#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import flask

import app
import app.fs
import app.res


@app.web.errorhandler(FileNotFoundError)
def page_not_found(exc):
    return flask.render_template(
        "stderror.html",
        title=app.res.PATHNOTFOUND_TITLE,
        message=app.res.PATHNOTFOUND_MSG_FORMAT.format(exc.filename)
    ), 404


@app.pageview(["/", "/files/", "/files/<path:path>"])
def retreive_dirlisting(path=""):
    path = app.fs.fullpath(path)
    try:
        files = [file.filename for file in app.fs.dirlisting(path)]
    except NotADirectoryError:
        return app.redirect(app.pages.file.retreive_fileview, path=path)
    title = '{} "{}"'.format(app.res.DIRECTORY_TITLE, path)
    return flask.render_template(
        "index.html",
        title=title,
        path=path,
        files=files
    )