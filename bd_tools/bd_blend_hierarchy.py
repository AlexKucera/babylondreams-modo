#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_blend_hierarchy

Release Notes:

    The command creates an easily animateable setup to dissolve/fade a hierarchy of items. By selecting the
    parent item and running the command a few things happen:

    1. A group with the whole item hierarchy gets created
    2. A shader setup gets created and put at the top of the shader tree
    3. The shader setup gets linked to the group


V0.1 Initial Release - 2017-02-20

"""

import modo
import lx
import traceback

import sys

from bd_tools import bd_helpers
from var import *


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(arbitrary=False, name=""):
    scene = modo.Scene()

    # Initialize values
    index = 10000000000000000000000  # Set the index to something very high so we can find the lowest index
    firstFrame = scene.renderItem.channel('first').get() / scene.fps
    func_name = BLEND_COMMAND
    blend_type = lx.eval("user.value bd.blend_type_pref ?")

    # Find the topmost spot below the renderOutputs
    for item in scene.renderItem.children():
        if item.type == "renderOutput":
            if index > item.parentIndex:
                index = item.parentIndex

    parentIndex = index

    if arbitrary:
        selected = scene.selected
        blend_name = '{1}_{0}'.format(name, func_name)
    else:
        selected = scene.selected[-1:]
        blend_name = '{1}_{0}'.format(selected[0].name, func_name)

    # Generate the complete hierarchy from the parent down and add it to a group
    hierarchy = []

    for select in selected:
        if select.type == "mesh":
            hierarchy.append(select)
        if select.type == "meshInst":
            hierarchy.append(select)
        for item in select.children(recursive=True):
            hierarchy.append(item)

    print hierarchy

    blend_group_name = '{0}_grp'.format(blend_name)

    try:

        scene.item(blend_group_name)
        modo.dialogs.alert('Warning',
                           '{0} already has a {1} group. Not creating a new one.'.format(selected[0].name, func_name),
                           dtype='warning')

    except:
        answer = "yes"
        groups = []
        check = False
        for item in hierarchy:
            for group in scene.getGroups('{0}'.format(func_name)):
                if group.hasItem(item):
                    check = True
                    groups.append(group.name)
            if check:
                answer = modo.dialogs.yesNo('Warning', '{0} is already in group(s) {1}. Do you still want to add it to '
                                                       'another group?'.format(item.name, groups))
                if answer == "no":
                    sys.exit()

        if answer == "no":
            None
        else:
            blend_group = scene.addGroup(name=blend_group_name, gtype='{0}'.format(func_name))
            blend_group.addItems(hierarchy)

            # Create a shading group, a shader and a constant
            mask = scene.addItem('mask', name='{0}_msk'.format(blend_name))
            shader = scene.addItem('defaultShader', name='{0}_shdr'.format(blend_name))
            constant = scene.addItem('constant', name='{0}_cnstnt'.format(blend_name))

            # Parent everything to the shading group
            shader.setParent(mask)
            constant.setParent(mask, index=0)
            mask.setParent(scene.renderItem, index=parentIndex)

            # Set the correct Shading Effect
            constant.channel('effect').set(blend_type)
            constant.channel('value').set(0.0, time=firstFrame, key=True)

            # Adjust the Item dropdown in the shading group
            # (yes, it is reverse, we are actually setting the input of the group to be the shading group)
            blend_group.itemGraph('shadeLoc').connectInput(mask)

            # Check if the Channel Set exist if not create it and add our new blend channel to it
            chan_set = False
            for group in scene.getGroups(gtype='chanset'):

                if group.name == '{}_channel_set'.format(func_name):
                    chan_set = True

            if not chan_set:
                chan_set = scene.addGroup(name='{}_channel_set'.format(func_name), gtype='chanset')
            else:
                chan_set = scene.item('{}_channel_set'.format(func_name))

            chan_set.addChannel('value', constant)


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
