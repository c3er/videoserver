#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import subprocess
import re
import json

import misc


VCODEC = "h264"
ACODEC = "aac"

_OUTPUTDIR = "output"
_OUTPUTFILE = "out.mp4"


_outputdir = os.path.join(misc.getstarterdir(), _OUTPUTDIR)

_transcoder = None


class Transcoder:
    def __init__(self, inputpath, outputpath):
        self.inputpath = inputpath
        self.outputpath = outputpath
        self._process = None
        self._isready = False

    def isrunning(self):
        if self._process is None or self._isready:
            return False
        if self._process.poll() is not None:
            self._isready = True
            return False
        return True

    def fits(self, path):
        return path == self.inputpath

    def isready(self):
        return self._isready

    def start(self):
        os.makedirs(_outputdir, exist_ok=True)
        self._process = subprocess.Popen(
            [
                "ffmpeg",
                "-hide_banner",
                "-i", self.inputpath,
                "-y",
                "-map", "0",
                "-vcodec", VCODEC,
                "-acodec", ACODEC,
                self.outputpath
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def stop(self):
        self._process.kill()


def get_transcoder(path):
    global _transcoder
    outputpath = os.path.join(_outputdir, _OUTPUTFILE)
    if not _transcoder:
        _transcoder = Transcoder(path, outputpath)
    elif not _transcoder.fits(path):
        _transcoder.stop()
        _transcoder = Transcoder(path, outputpath)
    return _transcoder


def getcodec(path):
    vcodec = None
    acodec = None

    completed_process = subprocess.run(
        [
            "ffprobe",
            "-hide_banner",
            "-print_format", "json",
            "-show_streams",
            path
        ],
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = _sanitize_json(completed_process.stdout)

    data = json.loads(output)
    stream_data = data["streams"]
    for stream_entry in stream_data:
        codec_type = stream_entry["codec_type"]
        codec = stream_entry["codec_name"]
        if codec_type == "video":
            vcodec = codec
        elif codec_type == "audio":
            acodec = codec

    return vcodec, acodec


def _sanitize_json(text):
    match = re.search(r'^{([\s\S]*)"streams"', text)
    return text.replace(match.group(1), "")


def _istranscoding():
    return _transcoder is not None and _transcoder.isrunning()
