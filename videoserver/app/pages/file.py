#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import flask

import app
import app.res


@app.pageview(["/fileview/", "/fileview/<path:path>"])
def retreive_fileview(path=""):
    if path:
        if not os.path.exists(path):
            error = FileNotFoundError()
            error.filename = path
            raise error
        title = '{} "{}"'.format(app.res.FILEVIEW_TITLE, path)
        return flask.render_template(
            "file.html",
            title=title,
            filename=path
        )
    else:
        return app.redirect(app.pages.index.retreive_dirlisting, path=path)