#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_parent_to_group

Release Notes:

V0.1 Initial Release - 2018-05-29

Copyright 2018 - BabylonDreams - Alexander Kucera & Monika Kucera GbR

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


"""

import os
import traceback

import lx
import modo

import bd_helpers
from var import *


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(group=None, parent_in_place=True, ui=True):
    start_timer = bd_helpers.timer()

    scene = modo.Scene()
    selected_items = scene.selected

    if ui:
        try:
            group = scene.item(group)  # find the item that is using the provided ID
        except:
            group = scene.addItem(lx.symbol.sITYPE_GROUPLOCATOR,
                                  group)  # create empty group in case we don't find the new group
    else:
        if selected_items[-1].type == lx.symbol.sITYPE_GROUPLOCATOR:
            group = selected_items.pop()
        else:
            group = scene.addItem(lx.symbol.sITYPE_GROUPLOCATOR)

    parents_group = []

    for item in selected_items:
        # here we check if a selected item has any parents
        # then we walk up the hierarchy until we find the
        # topmost selected parent and add that to the parents_group
        selection_parent = item
        print(item.parents)
        if item.parents:
            for parent in item.parents:
                if parent in selected_items:
                    selection_parent = parent
        parents_group.append(selection_parent)
    parents_group = set(parents_group)

    for item in parents_group:
        if parent_in_place:
            # parent slow, but keep transforms
            lx.eval('item.parent %s %s inPlace:1' % (item.id, group.id))
        else:
            # parent fast, but loose transforms
            item.setParent(newParent=group)

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
        print(traceback.format_exc())
