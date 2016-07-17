#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import optparse
import flask     # pip install Flask


DEFAULT_PORT = 3030


app = flask.Flask(__name__)



# Handlers #####################################################################

@app.route("/")
def hello():
    return '<html><body><h1>Hello web server</h1></body></html>'

################################################################################


# Helper functions #############################################################

def get_option_count(options):
    opt_count = 0
    for val in options.__dict__.values():
        if val is not None:
            opt_count += 1
    return opt_count

################################################################################


def main():
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
        dest='root_path',
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
            
    if options.root_path:
        root_path = options.root_path
        if not os.path.isdir(root_path):
            parser.error('Given path "{}" does not lead to a directory.'.format(root_path))
        if len(root_path) > 0 and not root_path.endswith('/'):
            root_path += '/'
    else:
        root_path = ''
    ############################################################################

    app.run(port=port)


if __name__ == "__main__":
    main()