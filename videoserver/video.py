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


class Transcoder:
    def __init__(self, inputpath, outputpath):
        self.outputpath = outputpath

        self._process = subprocess.Popen(
            [
                "ffmpeg",
                "-hide_banner",
                "-i", inputpath,
                "-y",
                "-map", "0",
                "-vcodec", VCODEC,
                "-acodec", ACODEC,
                outputpath
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def isrunning(self):
        return self._process.poll() is None

    def stop(self):
        self._process.kill()


def start_transcoding(path):
    os.makedirs(_outputdir, exist_ok=True)
    return Transcoder(path, os.path.join(_outputdir, _OUTPUTFILE))


def _sanitize_json(text):
    match = re.search(r'^{([\s\S]*)"streams"', text)
    return text.replace(match.group(1), "")


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
        universal_newlines=True
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
