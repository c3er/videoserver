#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app
import app.res


@app.pageview(["/fileview/<path:path>"])
def retreive_fileview(path=""):
    title = '{} "{}"'.format(app.res.FILEVIEW_TITLE, path)
    return flask.render_template(
        "file.html",
        title=title,
        filename=path
    )