#!/usr/bin/env python
# -*- coding: utf-8 -*-


import app


@app.servicehandler(app.services.video)
def get_video(file):
    return file
