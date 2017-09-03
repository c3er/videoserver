#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app
import app.fs


@app.servicehandler(app.services.filecontent)
def get_filecontent(path):
    file = app.fs.getfile(path)
    if file.isdir():
        error = IsADirectoryError()
        error.filename = path
        raise error
    return flask.send_file(file.ospath, mimetype="video/mp4")
