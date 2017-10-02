#!/usr/bin/env python
# -*- coding: utf-8 -*-


import flask

import app
import app.fs
import app.res

import video


@app.servicehandler(app.services.fileview)
def retreive_fileview(path=""):
    file = app.fs.getfile(path)
    if not file.isfile():
        return app.redirect(app.services.dirlisting, path=path)
    title = '{} "{}"'.format(app.res.FILEVIEW_TITLE, file.view_url)
    return flask.render_template(
        "fileview.html",
        title=title,
        file=file
    )


@app.servicehandler(app.services.filecontent)
def get_filecontent(path):
    file = app.fs.getfile(path)

    if file.isdir():
        error = IsADirectoryError(path)
        error.filename = path
        raise error

    if not file.iswebvideo():
        transcoder = video.get_transcoder(file.ospath)
        if transcoder.isready():
            file = app.fs.getfile(transcoder.outputpath)
        else:
            transcoder.start()
            return app.redirect(app.services.fileinfo, path=path)

    return flask.send_file(file.ospath, mimetype="video/mp4")


@app.servicehandler(app.services.fileinfo)
def get_fileinfo(path):
    return app.fs.FileStatus(video.get_transcoder())
