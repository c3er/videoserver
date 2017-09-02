#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app
import app.fs
import app.res


@app.servicehandler(app.services.dirlisting)
def retreive_dirlisting(path=""):
    dir = app.fs.getfile(path)
    if not dir.isdir():
        return app.redirect(app.services.fileview, path=path)
    files = dir.listdirs() + dir.listvideos()
    title = '{} "{}"'.format(app.res.DIRECTORY_TITLE, path)
    return flask.render_template(
        "index.html",
        title=title,
        path=path,
        files=files
    )
