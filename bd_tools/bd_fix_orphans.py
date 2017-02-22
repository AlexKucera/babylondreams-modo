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

import modo
import lx
import traceback


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():

    scene = modo.Scene()
    for item in scene.items():
        if item.superType == 'textureLayer' and item.type != 'shaderFolder':
            print item, item.parent
            if not item.parent:
                item.setParent(scene.renderItem)


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
