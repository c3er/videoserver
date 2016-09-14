#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import flask

import app

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

    def __init__(self, filepath, filename):
        self.filepath = filepath
        self.filename = filename

    @property
    def path(self):
        return os.path.join(self.filepath, self.filename)

    def isdir(self):
        return os.path.isdir(self.path)

    def isfile(self):
        return os.path.isfile(self.path)

    def isvideo(self):
        for filetype in self._known_videofiles:
            if self.isfile() and self.filename.endswith(filetype):
                debug("True:", self.filename)
                return True
        debug("False:", self.filename)
        return False


def fullpath(path):
    return os.path.join(app.rootpath, path)


def dirlisting(path):
    return [FileObject(path, file) for file in os.listdir(path)]
