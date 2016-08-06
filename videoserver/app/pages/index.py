#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO
# - Reasonable distinction between directories and supported files


import os
import flask

import app
import app.res

from misc import debug


_known_videofiles = (
    ".avi",
    ".mkv",
    ".mp4",
    ".mpg",
    ".divx",
)


class FileObject:
    def __init__(self, filepath, filename):
        self.filepath = filepath
        self.filename = filename

    @property
    def path(self):
        return os.path.join(self.filepath, self.filename)

    def isdir(self):
        return os.path.isdir(self.path)

    def isfile(self):  # Not really used yet
        return os.path.isfile(self.path)

    def isvideo(self):
        for filetype in _known_videofiles:
            if self.isfile() and self.filename.endswith(filetype):
                debug("True:", self.filename)
                return True
        debug("False:", self.filename)
        return False


def fullpath(path):
    return os.path.join(app.rootpath, path)


def dirlisting(path):
    files = (FileObject(path, file) for file in os.listdir(path))
    files = [file for file in files if file.isvideo()]
    return files


@app.pageview(["/", "/files/", "/files/<path:path>"])
def retreive_dirlisting(path=""):
    path = fullpath(path)
    try:
        files = [file.filename for file in dirlisting(path)]
    except NotADirectoryError:
        raise
    title = '{} "{}"'.format(app.res.DIRECTORY_TITLE, path)
    return flask.render_template(
        "index.html",
        title=title,
        path=path,
        files=files
    )