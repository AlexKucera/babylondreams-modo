#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_dissolve_hierarchy

Release Notes:

V0.1 Initial Release - 2017-02-20

"""

import modo
import lx
import traceback
from bd_tools import bd_helpers


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():
    scene = modo.Scene()
    index = 10000000000000000000000

    for item in scene.renderItem.children():
        if item.type == "renderOutput":
            if index > item.parentIndex:
                index = item.parentIndex

    parentIndex = index

    selected = bd_helpers.selected(1)
    blend_name = 'blend_{0}'.format(selected[0].name)

    hierarchy = [selected[0]]

    for item in selected[0].children():
        hierarchy.append(item)

    blend_group = scene.addGroup(name='{0}_grp'.format(blend_name))
    blend_group.addItems(hierarchy)

    mask = scene.addItem('mask', name='{0}_msk'.format(blend_name))
    shader = scene.addItem('defaultShader', name='{0}_shdr'.format(blend_name))
    item = scene.addItem('constant', name='{0}_cnstnt'.format(blend_name))

    shader.setParent(mask)
    item.setParent(mask, index=0)
    mask.setParent(scene.renderItem, index=parentIndex)

    item.channel('effect').set('tranAmount')
    item.channel('value').set(0)

    blend_group.itemGraph('shadeLoc').connectInput(mask)

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
