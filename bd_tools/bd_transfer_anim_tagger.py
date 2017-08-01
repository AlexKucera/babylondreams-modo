#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
BabylonDreams-modo-Kit - bd_transfer_anim_tagger

Release Notes:
    Tag a bunch of items in a scene for automatic animation transfer.

V0.1 Initial Release - 2017-02-13

"""

import hashlib
import time
import traceback

import lx
import modo

# These channels show up as animated even if there are no keys on them. Not a reliable source to determin animation.
forbidden_channels = ["localMatrix", "wposMatrix", "wrotMatrix", "wsclMatrix", "wpivPosMatrix", "wpivRotMatrix",
                      "worldMatrix", "glstate", "crvGroup", "matrix", "wParentMatrix", "glsurf", "mesh"]


# FUNCTIONS -----------------------------------------------

def list():
    print("Listing animated items without an animation tag.")

    untagged = []

    for item in selected:
        animated = False

        # find only animated items as we don't want to tag static ones and make the scene unnecessarily heavy.

        # first check the item's channels
        for channel in item.channels():
            if channel.name not in forbidden_channels:
                if channel.isAnimated:
                    animated = True

        # then check any transforms connected to the item as they don't show up under the item's channels
        for transform in item.transforms:
            for channel in transform.channels():
                if channel.name not in forbidden_channels:
                    if channel.isAnimated:
                        animated = True
        if animated:
            if item.hasTag("anim"):
                if not item.readTag("anim"):
                    untagged.append(item.name)
            else:
                untagged.append(item.name)

    if len(untagged) > 0:
        message = ""
        for item in untagged:
            message = "{}\n{}".format(message, item)
        modo.dialogs.alert("List of untagged items",
                       "The following items have animation on them, but are not tagged. "
                       "You might want to update your asset before importing it.\n{}".format(message),
                       dtype='info')
    else:
        modo.dialogs.alert("You are good to go!",
                           "Congratulations. All animated items have tags on them.",
                           dtype='info')


def assign():
    modo.dialogs.alert("Not done yet!",
                       "Sorry. This function is not implemented yet.",
                       dtype='info')
    #modo.dialogs.fileOpen('text', title='Open List of Tags', multi=False)


def update():
    for item in selected:

        createTag = False

        if item.hasTag("anim"):
            if not item.readTag("anim"):
                createTag = True
        else:
            createTag = True

        if createTag:
            tag(item)


def overwrite():
    for item in selected:
        tag(item)


def tag(item):
    print("Creating unique identifier.")
    # Creating unique identifier with a hash and the current time
    message = "{} {}".format(item.id, time.time())
    m = hashlib.sha1()
    m.update(message)
    digest = m.hexdigest()

    item.setTag("anim", "{}_{}".format(item.name, digest[:4]))


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(mode="update"):
    global scene
    global selected

    scene = modo.Scene()
    selected = scene.selected

    if mode == "assign":
        assign()

    if mode == "list":
        list()

    if mode == "update":

        if len(selected) == 0:
            modo.dialogs.alert("Warning", "Please select at least one item.", dtype='warning')

        update()

    if mode == "overwrite":

        if len(selected) == 0:
            modo.dialogs.alert("Warning", "Please select at least one item.", dtype='warning')

        overwrite()


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
