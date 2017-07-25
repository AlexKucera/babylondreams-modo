#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
BabylonDreams-modo-Kit - bd_transfer_anim

Release Notes:
    Copy the animation from one selected item to another. It will copy all animated channels from the
    first object to the second object. Any channels that are missing on the second object will be listed
    at the end for manual fixing. Please make sure you have Warning dialogs enabled in modo, otherwise the user
    won't get a popup dialog.

V0.1 Initial Release - 2017-02-13

"""

import modo
import lx
import traceback
from pprint import pprint

from bd_tools import bd_helpers
import bd_transfer_anim


# FUNCTIONS -----------------------------------------------

def get_tags(item):

    if item.hasTag("anim"):
        if item.readTag("anim"):
            tag = item.readTag("anim")
            return tag
    return None

# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():

    scene = modo.Scene()
    selected = bd_helpers.selected(2)

    sourceGroup = selected[0]
    targetGroup = selected[1]

    tagsSource = dict()
    for child in sourceGroup.children(recursive=True):
        tag = get_tags(child)
        tagsSource[tag] = child

    tagsTarget = dict()
    for child in targetGroup.children(recursive=True):
        tag = get_tags(child)
        tagsTarget[tag] = child

    tagMismatch = []
    for tag in tagsSource:
        print tag
        if tag in tagsTarget:
            print("{1} → {0}".format(tagsTarget[tag].name,tagsSource[tag].name) )
            reload(bd_transfer_anim)
            bd_transfer_anim.main(source=tagsSource[tag], target=tagsTarget[tag])
        else:
            tagMismatch.append(tagsSource[tag].name)

    if len(tagMismatch) > 0:
        message = ""
        for tag in tagMismatch:
            message = "{}\n{}".format(message, tag)
        modo.dialogs.alert("Warning",
                           "There were animated items that could not be matched to any items in the target.\n"
                           "Check their anim tag. Maybe it is missing or there is a mismatch.\n"
                           "{}".format(message), dtype='warning')


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
