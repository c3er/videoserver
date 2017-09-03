#!/usr/bin/env python
# -*- coding: utf-8 -*-


import app


@app.servicehandler(app.services.filecontent)
def get_filecontent(path):
    return path
