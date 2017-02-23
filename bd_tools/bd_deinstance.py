#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_deinstance

Release Notes:

V0.1 Initial Release - 2017-02-23

"""

import modo
import lx
import traceback


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():
    scene = modo.Scene()

    i = 0
    instance_types = []
    items = []
    for item in scene.selected:
        if item.isAnInstance:
            scene.select(item)

            if item.type == "meshInst":
                lx.eval("item.setType mesh")
            else:
                lx.eval("item.setType {0}".format(item.type))

            i += 1
            items.append(item.name)
            instance_types.append(item.type)
    output = ["{0} Instances de-instanced.\n\n".format(i)]
    for instance_type in set(instance_types):
        out = "{0} {1}s".format(instance_types.count(instance_type), instance_type)
        output.append(out)
    message = "\n".join(output)
    modo.dialogs.alert("De-instance complete", message, dtype='info')


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
