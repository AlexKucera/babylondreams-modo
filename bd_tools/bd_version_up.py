#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_version_up

Release Notes:

V0.1 Initial Release - 2017-08-15

"""

import bd_helpers
import modo
import lx
import traceback
import sys
import re

import imp

try:
    imp.find_module('lx.symbol')
    import lx.symbol
except ImportError:
    pass

from var import *


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(comment=False, commentstring=""):
    start_timer = bd_helpers.timer()

    scene = modo.Scene()
    regex = "(.+)_v(\d+)(\w+)?"  # Grab anything that has a character sequence followed by a _v and some number

    filepath = scene.filename
    if filepath:
        filename = os.path.splitext(os.path.basename(filepath))
        filepath = os.path.dirname(filepath)
        fileextension = filename[1]
        filename = filename[0]

        match = re.match(regex, filename)
        if match:
            version = match.group(2)
            filename = match.group(1)
            filecomment = match.group(3)

            result = "yes"
        else:
            message = "The provided file ({}{}) contains no version info (we are looking for a '_v000' here).\n\n" \
                      "Do you want to start versioning this file?".format(filename, fileextension)
            result = modo.dialogs.yesNo("Missing Version", message)

            if result == "yes":
                version = "00"

        if result == "yes":

            print('Current file "{}" is at Version {}.'.format(filename, version))

            created = False
            zfill = len(version)

            if comment:
                filecomment = commentstring.replace(" ","_").lower()
                filecomment = bd_helpers.format_filename(filecomment)
            else:
                filecomment = False

            while created is False:

                version = str(int(version) + 1).zfill(zfill)

                if filecomment:
                    newfile = os.path.join(filepath, "{}_v{}_{}{}".format(filename, version, filecomment, fileextension))
                else:
                    newfile = os.path.join(filepath, "{}_v{}{}".format(filename, version, fileextension))

                if os.path.isfile(newfile):
                    print("Version " + version + " already exists. Increasing version count.")
                    pass
                else:
                    print("Saving as Version " + version)
                    try:
                        lx.eval('scene.saveAs {%s}' % newfile)
                    except:
                        lx.eval('layout.createOrClose EventLog "Event Log_layout" '
                                'title:@macros.layouts@EventLog@ width:600 height:600 persistent:true '
                                'open:true')
                        print("ERROR Scene save failed with ", sys.exc_info())

                    created = True

    else:
        message = "The provided file has not been saved yet."
        modo.dialogs.alert("Missing Version!",
                           message,
                           dtype='error')

    bd_helpers.timer(start_timer, ' Overall')


# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':
    # Argument parsing is available through the 
    # lx.arg and lx.args methods. lx.arg returns 
    # the raw argument string that was passed into 
    # the script. lx.args parses the argument string 
    # and returns an array of arguments for easier 
    # processing.

    argsAsString = lx.arg()
    argsAsTuple = lx.args()

    try:
        main()
    except:
        print traceback.format_exc()
