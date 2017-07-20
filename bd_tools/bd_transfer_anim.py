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


# FUNCTIONS -----------------------------------------------

def get_channels(item, type=None, forbidden_channels=[], isAnimated=False):
    item_channels = []
    for channel in item.channels():
        if channel.name not in forbidden_channels:
            if type is "name":
                item_channels.append(channel.name)
            if type is "index":
                item_channels.append((channel.index))
            if type is None:
                pass
    if type is None:
        item_channels = item.channels()
    return item_channels


def channel_copy_paste(item_id, channel_name, cmd="copy"):
    lx.eval("select.channel {{{0}:{1}}} set".format(item_id, channel_name))
    if cmd is "paste":
        lx.eval("channel.paste")
    elif cmd is "copy":
        lx.eval("channel.copy")


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(source=None, target=None):
    # These channels show up as animated even if there are no keys on them. Not a reliable source to determin animation.
    forbidden_channels = ["localMatrix", "wposMatrix", "wrotMatrix", "wsclMatrix", "wpivPosMatrix", "wpivRotMatrix",
                          "worldMatrix", "glstate", "crvGroup", "matrix"]
    scene = modo.Scene()

    if source == None or target == None:
        selected = bd_helpers.selected(2)

        source = selected[0]
        target = selected[1]


    source_channels = get_channels(source, type="name", forbidden_channels=forbidden_channels, isAnimated=False)
    target_channels = get_channels(target, type="name", forbidden_channels=forbidden_channels, isAnimated=False)

    differences = list(set(source_channels) - set(target_channels))

    for difference in differences:
        forbidden_channels.append(difference)

    for channel in source.channels():
        if channel.isAnimated:
            if channel.name not in forbidden_channels:
                if channel.envelope.keyframes.numKeys > 0:
                    pprint(channel.name)
                    channel_copy_paste(source.id, channel.name, cmd="copy")
                    channel_copy_paste(target.id, channel.name, cmd="paste")

    for source_transform in source.transforms:
        source_transform_type = source_transform.type
        exists = False

        for target_transform in target.transforms:
            if target_transform.type == source_transform_type:
                exists = True
                target_transform_id = target_transform.id

        if not exists:
            target_transform_id = target.transforms.insert(source_transform_type)
            target_transform_id = target_transform_id.id

        for channel in source_transform.channels():
            if channel.isAnimated:
                if channel.name not in forbidden_channels:
                    if channel.envelope.keyframes.numKeys > 0:
                        channel_copy_paste(source_transform.id, channel.name, cmd="copy")
                        channel_copy_paste(target_transform_id, channel.name, cmd="paste")

    if len(differences) != 0:
        warning = "The following channels could not be copied because they do not exist on the target item:\n{0}".format(
        differences)
        modo.dialogs.alert("Warning", warning, dtype='warning')


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
