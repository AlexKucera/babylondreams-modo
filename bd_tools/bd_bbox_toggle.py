#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_bbox_toggle

Release Notes:

V0.1 Initial Release - 2017-03-08

"""

import bd_helpers
import modo
import lx
import traceback

from var import *


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(state='custom'):

    start_timer = bd_helpers.timer()

    scene = modo.Scene()
    selected = scene.selected
    drawShape = state  # default / custom
    if len(selected) == 0:
        for item in scene.iterItemsFast(itype='meshInst'):
            item.channel('drawShape').set(drawShape)
    else:
        for item in selected:

            if item.type == "meshInst":
                item.channel('drawShape').set(drawShape)

            for child in item.children(recursive=True, itemType='meshInst'):
                child.channel('drawShape').set(drawShape)

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
