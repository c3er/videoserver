#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app
import app.fs
import app.res


@app.servicehandler(app.services.fileview)
def retreive_fileview(path=""):
    file = app.fs.getfile(path)
    if not file.isfile():
        return app.redirect(app.services.dirlisting, path=path)
    title = '{} "{}"'.format(app.res.FILEVIEW_TITLE, file.url)
    return flask.render_template(
        "file.html",
        title=title,
        file=file
    )
