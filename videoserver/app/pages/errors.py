#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app.res
import misc


@app.web.errorhandler(FileNotFoundError)
def page_not_found(exc):
    return flask.render_template(
        "pathnotfound.html",
        title=app.res.NOTFOUND_TITLE,
        path=exc.filename
    ), 404