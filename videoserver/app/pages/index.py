#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import flask

import app


MAIN_TITLE = "Video Server"


def fullpath(path):
    return os.path.join(app.rootpath, path)

def dirlisting(path):
    return os.listdir(path)


@app.pageview(["/", "/files/", "/files/<path>"])
def retreive_fileobj(path=""):
    path = fullpath(path)
    files = dirlisting(path)
    return flask.render_template(
        "index.html",
        main_title=MAIN_TITLE,
        path=path,
        files=files
    )