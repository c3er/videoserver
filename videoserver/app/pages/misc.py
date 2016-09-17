#!/usr/bin/env python
# -*- coding: utf-8 -*-


import app


@app.servicehandler(app.services.root)
def get_root():
    return app.redirect(app.services.dirlisting)
