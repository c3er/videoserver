#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import flask

import app
import app.fs
import app.res


@app.pageview(app.urls.dirlisting)
def retreive_dirlisting(path=""):
    dir = app.fs.getfile(path)
    try:
        files = dir.listdirs() + dir.listvideos()
    except NotADirectoryError:
        return app.redirect(app.pages.file.retreive_fileview, path=path)
    else:
        title = '{} "{}"'.format(app.res.DIRECTORY_TITLE, path)
        return flask.render_template(
            "index.html",
            title=title,
            path=path,
            files=files
        )