#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import importlib
import flask

import misc


web = None
rootpath = None
services = None


class servicehandler:
    def __init__(self, s):
        assert isinstance(s, _ServiceData)
        self.decorators = [web.route(url) for url in s.urls]
        self.service = s
        
    def __call__(self, func):
        for decorator in self.decorators:
            func = decorator(func)
        self.service.func = func
        return func


def redirect(service, **kwargs):
    assert isinstance(service, _ServiceData)
    url = flask.url_for(service.func.__name__, **kwargs)
    return flask.redirect(url)


def init(port, root):
    global rootpath
    rootpath = root
    web.run(port=port)


_initialized = False


class _ServiceData:
    def __init__(self, urls):
        assert misc.islistlike(urls)
        self.urls = urls
        self.func = None
        self.urlbase = None


class _ServiceManager:
    def __init__(self):
        jsonpath = os.path.join(misc.getscriptpath(__file__), "services.json")
        with open(jsonpath, encoding="utf-8-sig") as f:
            servicedata = json.load(f)
        for member, urls in servicedata.items():
            setattr(self, member, _ServiceData(urls))


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
    services = _ServiceManager()
    _import_pages()

    _initialized = True