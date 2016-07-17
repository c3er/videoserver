#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

from appinit import app


@app.route("/test")
def test():
    return flask.render_template(
        "main.html",
        main_title="Test",
        root_path="Hallo Welt!"
    )