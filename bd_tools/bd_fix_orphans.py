#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_fix_orphans

Release Notes:

    Finds any Shader Tree items that have become unparented had parents them back to the Shader Tree.

    Workaround for http://modo.beta.thefoundry.co.uk/bug/view.aspx?TaskID=50149

V0.1 Initial Release - 2017-02-22

"""

import os
import traceback

import lx
import modo

from bd_tools import bd_helpers


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():
    start = bd_helpers.timer()
    scene = modo.Scene()

    for item in scene.iterItemsFast(lx.symbol.sITYPE_TEXTURELAYER):
        if item.superType == lx.symbol.sITYPE_TEXTURELAYER and item.type != lx.symbol.sITYPE_SHADERFOLDER:
            if not item.parent:
                print("Re-parenting {} to Shader Tree.".format(item.name))
                item.setParent(scene.renderItem)

    bd_helpers.timer(start, os.path.splitext(os.path.basename(__file__))[0])


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
