#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json

import app
import video
from misc import debug


class FileObject:
    _known_videofiles = (
        ".avi",
        ".mkv",
        ".mp4",
        ".mpg",
        ".mpeg",
        ".divx",
        ".flv",
        ".3gp",
    )

    def __init__(self, name, parent=None):
        assert isinstance(name, str)
        assert isinstance(parent, (type(None), FileObject))
        
        self.parent = parent
        self.name = name
        self._fullpath = ""

    @property
    def view_url(self):
        return self._getserviceurl(self._getviewservice())

    @property
    def content_url(self):
        if self.isvideo():
            return self._getserviceurl(app.services.filecontent)

    @property
    def info_url(self):
        if self.isvideo():
            return self._getserviceurl(app.services.fileinfo)

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

        return self._fullpath.replace("\\", "/")

    def isdir(self):
        return os.path.isdir(self.ospath)

    def isfile(self):
        return os.path.isfile(self.ospath)

    def isvideo(self):
        if not self.isfile():
            return False
        return any(self.name.endswith(filetype) for filetype in self._known_videofiles)

    def iswebvideo(self):
        if not self.isvideo():
            return False
        return video.getcodec(self.ospath) == (video.VCODEC, video.ACODEC)

    def list(self):
        return [FileObject(path, self) for path in os.listdir(self.ospath)]

    def listdirs(self):
        return [file for file in self.list() if file.isdir()]

    def listvideos(self):
        return [file for file in self.list() if file.isvideo()]

    def _getviewservice(self):
        return app.services.dirlisting if self.isdir() else app.services.fileview

    def _getserviceurl(self, service):
        return self.ospath.replace(
            app.rootpath.replace("\\", "/"),
            service.urlbase[:-1]
        )


class FileStatus:
    def __init__(self, transcoder):
        self._transcoder = transcoder

    def tojson(self):
        return json.dumps({
            "isRunning": self._transcoder.isrunning(),
            "isReady": self._transcoder.isready(),
        })


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
