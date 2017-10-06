#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_collect_texturelocators

Release Notes:

V0.1 Initial Release - 2017-09-01

"""

import traceback

import lx
import modo

import bd_helpers
from var import *


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():
    start_timer = bd_helpers.timer()

    scene = modo.Scene()

    try:
        group = scene.item('textureLocators_group')
    except:
        group = scene.addItem(lx.symbol.sITYPE_GROUPLOCATOR, name='textureLocators_group')

    for i in scene.iterItemsFast(lx.symbol.sITYPE_TEXTURELOC):
        if not i.parent == group:
            print("Re-parenting {} to {}".format(i.name, group.name))
            i.setParent(newParent=group)

    bd_helpers.timer(start_timer, os.path.splitext(os.path.basename(__file__))[0])


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
