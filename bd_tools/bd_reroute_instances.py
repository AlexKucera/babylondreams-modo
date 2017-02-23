#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_reroute_instances

Release Notes:

V0.1 Initial Release - 2017-02-23

"""

import modo
import lx
import traceback


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(new_source, instances):
    scene = modo.Scene()
    new_source = scene.item(new_source)  # find the item that is using the provided ID
    print("#"*40)
    print "selected source: {0} ({1})".format(new_source.name, new_source.id)
    for instance in instances:
        # Transform connections first
        #print "source items: {0}".format(instance.itemGraph('source').connectedItems)
        new_source.itemGraph('source').connectInput(instance)
        #print "new source items: {0}".format(instance.itemGraph('source').connectedItems)

        # Now Mesh Connections
        print "meshInst items: {0}".format(instance.itemGraph('meshInst').connectedItems)
        instance.itemGraph('meshInst').connectInput(new_source)
        old_source = instance.itemGraph('meshInst').reverse()[0]
        print "meshInst old source: {0}".format(old_source.itemGraph('meshInst').connectedItems)
        print "new meshInst items: {0}".format(instance.itemGraph('meshInst').connectedItems)



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
