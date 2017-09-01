#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os

import log
import app
import config
import misc


LOGFILE = "server.log"


def main():
    args = sys.argv
    try:
        log.init(os.path.join(misc.getstarterdir(), LOGFILE), config.debug)

        if len(args) != 2:
            sys.exit("Root directory to serve needed as only parameter.")
        rootpath = args[1]

        log.info("Given path: " + rootpath)
        app.init(config.port, rootpath)
    except Exception as exc:
        log.exception(exc)
        raise
    finally:
        log.close()


if __name__ == "__main__":
    main()