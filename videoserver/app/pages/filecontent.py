#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app
import app.fs


@app.servicehandler(app.services.filecontent)
def get_filecontent(path):
    return flask.send_file(app.fs.getfile(path).ospath, mimetype="video/mp4")
