#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import optparse
import flask

import app
import app.misc


DEFAULT_PORT = 3030


# Helper functions #############################################################

def get_option_count(options):
    opt_count = 0
    for val in options.__dict__.values():
        if val is not None:
            opt_count += 1
    return opt_count

################################################################################


def main():
    global app_state

    # Evaluate given options ###################################################
    parser = optparse.OptionParser()
    parser.add_option(
        '-p',
        '--port',
        dest='port',
        help='Serverport. Default port is ' + str(DEFAULT_PORT)
    )
    parser.add_option(
        '-r',
        '--root',
        dest='rootpath',
        help='Root path. The default root path is the current directory.'
    )
    options, args = parser.parse_args()  # "args" not needed

    if get_option_count(options) == 0:
        parser.print_help()
    
    if options.port:
        try:
            port = int(options.port)
        except ValueError as exc:
            port = options.port
            parser.error('Could not identify "{}" as port.'.format(port))
    else:
        port = DEFAULT_PORT
            
    if options.rootpath:
        rootpath = options.rootpath
        if not os.path.isdir(rootpath):
            parser.error('Given path "{}" does not lead to a directory.'.format(rootpath))
        if len(rootpath) > 0 and not rootpath.endswith(("/", "\\")):
            rootpath += '\\'
    else:
        rootpath = app.misc.getscriptpath(__file__) + "\\"
    ############################################################################

    print("Given path:", rootpath)
    app.init(port, rootpath)


if __name__ == "__main__":
    main()