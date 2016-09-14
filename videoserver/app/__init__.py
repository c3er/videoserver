#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import importlib
import flask

import misc


_initialized = False


# Public #######################################################################

web = None
rootpath = None
urls = None


class pageview:
    def __init__(self, urls):
        assert misc.islistlike(urls)
        self.decorators = [web.route(url) for url in urls]
        
    def __call__(self, func):
        for decorator in self.decorators:
            func = decorator(func)
        return func


def redirect(func, **kwargs):
    url = flask.url_for(func.__name__, **kwargs)
    return flask.redirect(url)


def init(port, root):
    global rootpath
    rootpath = root
    web.run(port=port)
    
################################################################################


# Private ######################################################################

class _URLManager:
    def __init__(self):
        jsonpath = os.path.join(misc.getscriptpath(__file__), "urls.json")
        with open(jsonpath, encoding="utf-8-sig") as f:
            urldata = json.load(f)
        for member, urls in urldata.items():
            setattr(self, member, urls)


def _ispage(pagefile):
    return (
        pagefile.endswith(".py") and
        pagefile != "__init__.py"
    )


def _import_pages():
    pagepath = os.path.join(misc.getscriptpath(__file__), "pages")
    pagefiles = [pagefile for pagefile in os.listdir(pagepath) if _ispage(pagefile)]
    pages = [pagefile[:-3] for pagefile in pagefiles]
    for page in pages:
        importlib.import_module("app.pages." + page)


if not _initialized:
    web = flask.Flask(__name__)
    urls = _URLManager()
    _import_pages()

    _initialized = True
    
################################################################################