#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_reroute_instances

Release Notes:

    select as many instances as you want and execute the command. it will ask you for a new mesh source.
    pick one from the dropdown or put in a new name and an empty mesh will be created as new source.

V0.1 Initial Release - 2017-02-23

"""
import sys
import modo
import lx
import traceback


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------


def main(new_source):

    scene = modo.Scene()

    # appversion = lx.eval('query platformservice "appversion" ?')
    #
    # if appversion > 1021:
    #     modo.dialogs.alert('Error',
    #                        'This script only works in modo 10.2v1 and below. Sorry.',
    #                        dtype='error')
    #     sys.exit()

    items = scene.selected
    try:
        new_source = scene.item(new_source)  # find the item that is using the provided ID
    except:
        new_source = scene.addItem('mesh', new_source)  # create empty mesh in case we don't find the new source

    sources = []
    instances = []

    # Check if we have instances selected and weed out any non-instances in the process
    for item in items:
        if not item.isAnInstance:
            sources.append(item.name)
        else:
            instances.append(item)

    if len(instances) == 0:
        modo.dialogs.alert('Error',
                           'No Instances selected. Please select at least one instance.',
                           dtype='error')
        sys.exit()

    # And now for the fun part
    print "selected source: {0} ({1})".format(new_source.name, new_source.id)
    for instance in instances:

        # Disconnect any existing meshInst graph connections.
        for source in instance.itemGraph("meshInst").reverse():
            # << and disconnectInput do the same thing theoretically,
            # but I had one or the other break on me in the past, so
            # now I am including both just to make sure
            try:
                source.itemGraph("meshInst") << instance
            except:
                pass
            try:
                instance.itemGraph("meshInst").disconnectInput(source)
            except:
                pass

            # Disconnect any existing source graph connections.
            # Note that the meshInst graph and the source graph go
            # in different directions. That's why we cache the
            # "sourceGraph" in advance.
            sourceGraph = instance.itemGraph("source")
            for source in sourceGraph.forward():
                sourceGraph << source

            # Connect new prototype. Again, notice how they go in
            # different directions.
            instance >> new_source.itemGraph("source")
            new_source >> instance.itemGraph("meshInst")

            print "re-routing {0} from {1} to {2}".format(instance.name, source.name, new_source.name)

    if len(sources) > 0:
        modo.dialogs.alert('Warning',
                           'The following items are no instances and were skipped:\n{0}'.format(sources),
                           dtype='warning')

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
        main("newMesh")
    except:
        print traceback.format_exc()
