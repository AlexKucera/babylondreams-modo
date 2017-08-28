#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_overscan

Release Notes:

V0.1 Initial Release - 2017-08-28

"""
import re

import bd_helpers
import modo
import lx
import traceback

from var import *


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(mode='resolution',
         newsize='2016x1134'):

    regex = "(\d+)(?:\D+)(\d+)"

    start_timer = bd_helpers.timer()

    scene = modo.Scene()

    # Get current scene values
    old_width = scene.renderItem.channel(lx.symbol.sICHAN_POLYRENDER_RESX).get()
    old_height = scene.renderItem.channel(lx.symbol.sICHAN_POLYRENDER_RESY).get()

    old_apertureX = scene.renderCamera.channel(lx.symbol.sICHAN_CAMERA_APERTUREX).get()
    old_apertureY = scene.renderCamera.channel(lx.symbol.sICHAN_CAMERA_APERTUREY).get()

    print("Old Render Resolution: {}x{}px".format(old_width, old_height))
    print("Old Camera Aperture: {}mmx{}mm".format(old_apertureX, old_apertureY))

    if mode == "scale":

        try:
            scale = float(newsize.replace(",", "."))
            new_width = int(old_width * scale)
            new_height = int(old_height * scale)
        except:
            modo.dialogs.alert("Wrong Scale Format",
                               "Unable to parse the given scale. Please use a floating point number.",
                               dtype='error')

    else:

        try:
            float(newsize.replace(",", "."))
        except:
            match = re.match(regex, newsize)
            if match and len(match.groups()) == 2:

                new_width = int(match.group(1))
                new_height = int(match.group(2))

            else:
                modo.dialogs.alert(
                    "Wrong Resolution Format",
                    "Unable to parse the given resolution. Please use the format <width> x <height>.",
                    dtype='error'
                )

    # Apply Overscan formula to width and height
    new_apertureX = old_apertureX * (new_width / float(old_width))
    new_apertureY = old_apertureY * (new_height / float(old_height))

    # Set new scene values
    scene.renderItem.channel(lx.symbol.sICHAN_POLYRENDER_RESX).set(new_width)
    scene.renderItem.channel(lx.symbol.sICHAN_POLYRENDER_RESY).set(new_height)

    scene.renderCamera.channel(lx.symbol.sICHAN_CAMERA_APERTUREX).set(new_apertureX)
    scene.renderCamera.channel(lx.symbol.sICHAN_CAMERA_APERTUREY).set(new_apertureY)

    print("New Render Resolution: {}x{}px".format(new_width, new_height))
    print("New Camera Aperture: {}mmx{}mm".format(new_apertureX, new_apertureY))

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
