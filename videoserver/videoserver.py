#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import optparse
import flask

import app
import app.misc

import config


DEFAULT_PORT = 3030


# Helper functions #############################################################

def get_option_count(options):
    opt_count = 0
    for val in options.__dict__.values():
        if val is not None:
            opt_count += 1
    return opt_count

################################################################################


def main(args):
    if len(args) != 2:
        sys.exit("Root directory to serve needed as only parameter.")
    rootpath = args[1]
    print("Given path:", rootpath)
    app.init(config.port, rootpath)


if __name__ == "__main__":
    main(sys.argv)