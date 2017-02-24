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

     Only works in modo 10.2v1 and lower for now.

     Already bugged: http://modo.beta.thefoundry.co.uk/bug/view.aspx?TaskID=54793

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

    appversion = lx.eval('query platformservice "appversion" ?')

    if appversion > 1021:
        modo.dialogs.alert('Error',
                           'This script only works in modo 10.2v1 and below. Sorry.',
                           dtype='error')
        sys.exit()

    items = scene.selected
    try:
        new_source = scene.item(new_source)  # find the item that is using the provided ID
    except:
        new_source = scene.addItem('mesh', new_source)  # create empty mesh in case we don't find the new source yet

    source = []
    instances = []

    # Check if we have instances selected and weed out any non-instances in the process
    for item in items:
        if not item.isAnInstance:
            source.append(item.name)
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

        # Re-route transform connections first
        old_source = instance.itemGraph('source').forward()[0]
        old_source.itemGraph('source').disconnectInput(instance)
        new_source.itemGraph('source').connectInput(instance)

        # Now Mesh Connections
        instance.itemGraph('meshInst').disconnectInput(old_source)
        instance.itemGraph('meshInst').connectInput(new_source)

        print "re-routing {0} from {1} to {2}".format(instance.name, old_source.name, new_source.name)

    if len(source) > 0:
        modo.dialogs.alert('Warning',
                           'The following items are no instances and were skipped:\n{0}'.format(source),
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
        main()
    except:
        print traceback.format_exc()
