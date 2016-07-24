#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import optparse
import flask

import app
import app.misc

import config


def main(args):
    if len(args) != 2:
        sys.exit("Root directory to serve needed as only parameter.")
    rootpath = args[1]

    print("Given path:", rootpath)
    app.init(config.port, rootpath)


if __name__ == "__main__":
    main(sys.argv)