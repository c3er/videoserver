#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import flask

import app
import app.fs
import app.res


@app.pageview(app.urls.dirlisting)
def retreive_dirlisting(path=""):
    path = app.fs.fullpath(path)
    try:
        files = [
            file.filename
            for file in app.fs.dirlisting(path)
            if file.isvideo() or file.isdir()
        ]
    except NotADirectoryError:
        return app.redirect(app.pages.file.retreive_fileview, path=path)
    title = '{} "{}"'.format(app.res.DIRECTORY_TITLE, path)
    return flask.render_template(
        "index.html",
        title=title,
        path=path,
        files=files
    )