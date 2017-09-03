#!/usr/bin/env python
# -*- coding: utf-8 -*-


import app


@app.servicehandler(app.services.fileinfo)
def get_fileinfo(path):
    return path
