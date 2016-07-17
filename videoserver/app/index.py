#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import flask

import app


MAIN_TITLE = "Video Server"


def fullpath(path):
    return os.path.join(app.rootpath, path)


@app.web.route("/")
@app.web.route("/files/<path>")
def retreive_fileobj(path=""):
    return flask.render_template(
        "index.html",
        main_title=MAIN_TITLE,
        path=fullpath(path)
    )