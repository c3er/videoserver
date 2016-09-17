#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import flask

import app

import misc
from misc import debug


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
        self.name = name
        self._fullpath = ""

    @property
    def url(self):
        return (
            self.ospath
            .replace(app.rootpath, "")
            .replace("\\", "/")
        )

    @property
    def ospath(self):
        path = self.name
        parent = self.parent

        while parent:
            path = "/".join((parent.name, path))
            parent = parent.parent
        if path.startswith("/"):
            path = path[1:]

        self._fullpath = os.path.join(app.rootpath, path)
        if not os.path.exists(self._fullpath):
            error = FileNotFoundError()
            error.filename = self.name
            raise error

        return self._fullpath

    def isdir(self):
        return os.path.isdir(self.ospath)

    def isfile(self):
        return os.path.isfile(self.ospath)

    def isvideo(self):
        for filetype in self._known_videofiles:
            if self.isfile() and self.name.endswith(filetype):
                debug("app.fs.FileObject.isvideo: Is video:", self.ospath)
                return True
        debug("app.fs.FileObject.isvideo: Is not video:", self.ospath)
        return False

    def list(self):
        return [FileObject(path, self) for path in os.listdir(self.ospath)]

    def listdirs(self):
        return [file for file in self.list() if file.isdir()]

    def listvideos(self):
        return [file for file in self.list() if file.isvideo()]


def getfile(path):
    assert isinstance(path, str)
    assert "\\" not in path
    debug("app.fs.getfile: Given path:", path)

    if path.endswith("/"):
        path = path[:-1]

    parts = path.split("/")
    name = parts[-1]
    file = FileObject(name)

    if len(parts) > 1:
        currentfile = file
        parts = parts[:-1]
        while parts:
            currentfile.parent = FileObject(parts[-1])
            currentfile = currentfile.parent
            parts = parts[:-1]

    return file
