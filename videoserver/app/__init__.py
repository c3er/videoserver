#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import importlib
import flask

import misc
import app.state


rootpath = None

# Initialized while this file is imported at normal circumstances
web = None
services = None


class URLError(Exception): pass


class servicehandler:
    def __init__(self, service):
        assert isinstance(service, _ServiceData)
        self.decorators = [web.route(url) for url in service.urls]
        self.service = service
        
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


class ServiceManager:
    """Called while this file is imported at normal circumstances."""
    def __init__(self, jsonpath=os.path.join(misc.getscriptpath(__file__), "services.json")):
        with open(jsonpath, encoding="utf-8-sig") as f:
            servicedata = json.load(f)
        for member, urls in servicedata.items():
            setattr(self, member, _ServiceData(urls))
        self._data = servicedata

    def __len__(self):
        return len(list(iter(self)))

    def __iter__(self):
        members = (getattr(self, member) for member in dir(self))
        return iter(member for member in members if isinstance(member, _ServiceData))


class _ServiceData:
    def __init__(self, urls):
        assert misc.islistlike(urls)
        assert len(urls) > 0
        self.func = None
        self.urls, self.urlbase = self._prepare_urls(urls)

    @staticmethod
    def _prepare_urls(urls):
        urlbase = ""
        for url in urls:
            parts = url.split("/")
            if len(parts) < 2 and parts[0] != "":
                raise URLError("Given URL '{}' does not begin with '/'".format(url))
            tmpurlbase = parts[1]
            if not urlbase:
                urlbase = tmpurlbase
            if urlbase != tmpurlbase:
                raise URLError("It is allowed only to give the same base URL with optional parameters")
        if not urlbase.endswith("/"):
            urlbase += "/"
        return urls, "/" + urlbase


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


if not app.state.initialized:
    web = flask.Flask(__name__)
    services = ServiceManager()
    _import_pages()

    app.state.initialized = True
