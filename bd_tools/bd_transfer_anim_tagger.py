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

import modo
import lx
import traceback
import time
import hashlib

from pprint import pprint

from bd_tools import bd_helpers


# FUNCTIONS -----------------------------------------------

# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(mode="update"):
    # These channels show up as animated even if there are no keys on them. Not a reliable source to determin animation.
    forbidden_channels = ["localMatrix", "wposMatrix", "wrotMatrix", "wsclMatrix", "wpivPosMatrix", "wpivRotMatrix",
                          "worldMatrix", "glstate", "crvGroup", "matrix"]

    scene = modo.Scene()
    selected = scene.selected

    print mode

    if mode == "assign":

        modo.dialogs.fileOpen('text', title='Open List of Tags', multi=False)

    if mode == "list":
        print("Listing animated items without an animation tag.")

    if mode == "update" or mode == "overwrite":

        for item in selected:
            # animated = False
            #
            # # find only animated items as we don't want to tag static ones and make the scene unnecessarily heavy.
            #
            # # first check the item's channels
            # for channel in item.channels():
            #     if channel.name not in forbidden_channels:
            #         if channel.isAnimated:
            #             print channel.name
            #             animated = True
            #
            # # then check any transforms connected to the item as they don't show up under the item's channels
            # for transform in item.transforms:
            #     for channel in transform.channels():
            #         if channel.name not in forbidden_channels:
            #             if channel.envelope.keyframes.numKeys > 0:
            #                 print channel.name
            #                 animated = True
            animated = True
            if animated:

                createTag = False

                if mode == "update":
                    if item.hasTag("anim"):
                        if not item.readTag("anim"):
                            createTag = True
                    else:
                        createTag = True

                if mode == "overwrite":
                    print "er?"
                    createTag = True

                if createTag:
                    print("Creating unique identifier.")
                    # Creating unique identifier with a hash and the current time
                    message = "{} {}".format(item.id, time.time())
                    m = hashlib.sha1()
                    m.update(message)
                    digest = m.hexdigest()

                    item.setTag("anim", "{}_{}".format(item.name, digest[:4]))


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
