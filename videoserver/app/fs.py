#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import flask

import app

import misc
from misc import debug


class NotAFileError(Exception):
    pass


class FileObject:
    _known_videofiles = (
        ".avi",
        ".mkv",
        ".mp4",
        ".mpg",
        ".mpeg",
        ".divx",
        ".gif",
    )

    def __init__(self, name, parent=None):
        assert isinstance(name, str)
        assert isinstance(parent, (type(None), FileObject))
        self.parent = parent
        self._ospath = self._fullpath(name)
        debug("Path:", self._ospath)
        if not os.path.exists(self._ospath):
            error = FileNotFoundError()
            error.filename = name
            raise error

    @property
    def name(self):
        if not os.path.samefile(self._ospath, app.rootpath):
            return misc.getlastpathpart(self._ospath)
        return ""

    @property
    def url(self):
        return (
            self._ospath
            .replace(app.rootpath, "")
            .replace("\\", "/")
        )

    def isdir(self):
        return os.path.isdir(self._ospath)

    def isfile(self):
        return os.path.isfile(self._ospath)

    def isvideo(self):
        for filetype in self._known_videofiles:
            if self.isfile() and self.name.endswith(filetype):
                debug("Is video:", self._ospath)
                return True
        debug("Is not video:", self._ospath)
        return False

    def list(self):
        return [FileObject(path, self) for path in os.listdir(self._ospath)]

    def listdirs(self):
        return [file for file in self.list() if file.isdir()]

    def listvideos(self):
        return [file for file in self.list() if file.isvideo()]

    def _fullpath(self, name):
        path = name
        parent = self.parent
        while parent is not None:
            path = os.path.join(parent.name, name)
            parent = parent.parent
        return os.path.join(app.rootpath, path)


def getfile(path):
    assert isinstance(path, str)
    return FileObject(path)
