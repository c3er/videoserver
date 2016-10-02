#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

import log
import app
import config


LOGFILE = "server.log"


def main(args):
    try:
        log.init(LOGFILE, config.debug)

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
    main(sys.argv)