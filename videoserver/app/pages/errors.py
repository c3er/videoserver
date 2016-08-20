#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app.res
import misc


@app.web.errorhandler(404)
def page_not_found(exc):
    return flask.render_template(
        "404.html",
        title=app.res.ERROR404_TITLE,
        message=exc.description
    ), 404