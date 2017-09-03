#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app
import app.fs


BLOCKSIZE = 1024


@app.servicehandler(app.services.filecontent)
def get_filecontent(path):
    file = app.fs.getfile(path)

    # See http://flask.pocoo.org/docs/0.12/patterns/streaming/
    def generate():
        with open(file.ospath, "rb") as f:
            while True:
                data = f.read(BLOCKSIZE)
                if not data:
                    break
                yield data
    return flask.Response(generate(), mimetype='video/mp4')
